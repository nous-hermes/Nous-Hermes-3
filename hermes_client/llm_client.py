"""Inference client supporting Ollama and OpenAI-compatible endpoints with tool loops."""

from typing import List, Dict, Any, Optional
import json
import requests

from .config import AppConfig
from .tools import ToolRegistry


class HermesLLMClient:
    """Sends chat requests and handles multi-step function calling loops."""

    def __init__(self, config: AppConfig, tools: Optional[ToolRegistry] = None) -> None:
        self.config = config
        self.tools = tools

    def _chat_ollama(
        self, messages: List[Dict[str, Any]], use_tools: bool = True
    ) -> Dict[str, Any]:
        """Call Ollama /api/chat endpoint."""
        url = f"{self.config.base_url.rstrip('/')}/api/chat"
        payload: Dict[str, Any] = {
            "model": self.config.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": self.config.generation.temperature,
                "top_p": self.config.generation.top_p,
                "num_ctx": self.config.generation.context_length,
                "repeat_penalty": self.config.generation.repeat_penalty,
                "num_predict": self.config.generation.max_tokens,
            },
        }
        if self.config.generation.json_mode:
            payload["format"] = "json"
        if use_tools and self.tools and self.tools.schemas():
            payload["tools"] = self.tools.schemas()

        resp = requests.post(url, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        msg = data.get("message", {})
        return {
            "content": msg.get("content", ""),
            "tool_calls": msg.get("tool_calls", []),
        }

    def _chat_openai_compatible(
        self, messages: List[Dict[str, Any]], use_tools: bool = True
    ) -> Dict[str, Any]:
        """Call an OpenAI-compatible /v1/chat/completions endpoint."""
        url = f"{self.config.base_url.rstrip('/')}/v1/chat/completions"
        headers = {"Content-Type": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"

        payload: Dict[str, Any] = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.generation.temperature,
            "top_p": self.config.generation.top_p,
            "max_tokens": self.config.generation.max_tokens,
        }
        if self.config.generation.json_mode:
            payload["response_format"] = {"type": "json_object"}
        if use_tools and self.tools and self.tools.schemas():
            payload["tools"] = self.tools.schemas()

        resp = requests.post(url, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        choice = data["choices"][0]["message"]
        return {
            "content": choice.get("content") or "",
            "tool_calls": choice.get("tool_calls") or [],
        }

    def generate_with_tools(
        self, conversation: List[Dict[str, Any]], max_tool_rounds: int = 5
    ) -> Dict[str, Any]:
        """Run model inference and resolve any tool calls until a final answer is produced."""
        working_messages = list(conversation)
        tool_events: List[Dict[str, Any]] = []

        for _ in range(max_tool_rounds):
            if self.config.backend == "ollama":
                reply = self._chat_ollama(working_messages, use_tools=True)
            elif self.config.backend == "openai_compatible":
                reply = self._chat_openai_compatible(working_messages, use_tools=True)
            else:
                raise ValueError(f"Unsupported backend: {self.config.backend}")

            tool_calls = reply.get("tool_calls") or []
            if not tool_calls or not self.tools:
                return {
                    "content": reply.get("content", ""),
                    "tool_events": tool_events,
                }

            # Append assistant turn containing tool call intent
            working_messages.append(
                {
                    "role": "assistant",
                    "content": reply.get("content", ""),
                    "tool_calls": tool_calls,
                }
            )

            # Execute each tool call and feed the output back as a tool message
            for call in tool_calls:
                fn_block = call.get("function", call)
                fn_name = fn_block.get("name", "")
                raw_args = fn_block.get("arguments", {})
                if isinstance(raw_args, str):
                    try:
                        parsed_args = json.loads(raw_args) if raw_args else {}
                    except json.JSONDecodeError:
                        parsed_args = {}
                else:
                    parsed_args = raw_args or {}

                tool_output = self.tools.execute(fn_name, parsed_args)
                tool_events.append(
                    {
                        "name": fn_name,
                        "arguments": parsed_args,
                        "output": tool_output,
                    }
                )
                working_messages.append(
                    {
                        "role": "tool",
                        "name": fn_name,
                        "content": tool_output,
                    }
                )

        return {
            "content": "Max tool execution rounds reached without a final response.",
            "tool_events": tool_events,
        }
