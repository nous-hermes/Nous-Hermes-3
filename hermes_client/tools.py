"""Function calling (tool) registry, schemas, and local execution helpers."""

from datetime import datetime, timezone
from typing import Callable, Dict, Any, List
import json


class ToolRegistry:
    """Registers callable Python tools and exports OpenAI-compatible tool schemas."""

    def __init__(self) -> None:
        self._handlers: Dict[str, Callable[[Dict[str, Any]], Any]] = {}
        self._schemas: List[Dict[str, Any]] = []

    def register(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        handler: Callable[[Dict[str, Any]], Any],
    ) -> None:
        """Register a new tool with its JSON schema and handler function."""
        self._handlers[name] = handler
        self._schemas.append(
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": parameters,
                },
            }
        )

    def schemas(self) -> List[Dict[str, Any]]:
        """Return tool definitions to send to the model."""
        return self._schemas

    def execute(self, name: str, arguments: Dict[str, Any]) -> str:
        """Execute a registered tool and return a JSON-encoded result string."""
        if name not in self._handlers:
            return json.dumps({"error": f"Unknown tool: {name}"})
        try:
            result = self._handlers[name](arguments)
            return json.dumps({"result": result}, ensure_ascii=False)
        except Exception as exc:
            return json.dumps({"error": str(exc)}, ensure_ascii=False)


def _get_current_utc_time(_: Dict[str, Any]) -> str:
    return datetime.now(timezone.utc).isoformat()


def _calculate_expression(args: Dict[str, Any]) -> float:
    """Evaluate a basic arithmetic expression safely."""
    expr = str(args.get("expression", "")).strip()
    allowed_chars = set("0123456789+-*/(). ")
    if not expr or not set(expr).issubset(allowed_chars):
        raise ValueError("Unsupported characters in arithmetic expression.")
    return float(eval(expr, {"__builtins__": {}}, {}))


def build_default_tools() -> ToolRegistry:
    """Create a registry populated with starter tools."""
    registry = ToolRegistry()
    registry.register(
        name="get_utc_time",
        description="Get the current UTC timestamp in ISO-8601 format.",
        parameters={"type": "object", "properties": {}, "required": []},
        handler=_get_current_utc_time,
    )
    registry.register(
        name="calculator",
        description="Evaluate a basic arithmetic expression (+, -, *, /, parentheses).",
        parameters={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Arithmetic expression, e.g. '(128000 / 1024) * 2'.",
                }
            },
            "required": ["expression"],
        },
        handler=_calculate_expression,
    )
    return registry
