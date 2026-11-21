"""Configuration, onboarding workspace setup, and generation presets for Nous Hermes 3."""

from dataclasses import dataclass, field, asdict
from pathlib import Path
import json
from typing import Dict, Any


DEFAULT_WORKSPACE = Path.home() / ".hermes3_client"


@dataclass
class GenerationConfig:
    """Parameters controlling model sampling, context window, and output format."""

    temperature: float = 0.7
    top_p: float = 0.9
    max_tokens: int = 2048
    context_length: int = 128000
    repeat_penalty: float = 1.05
    json_mode: bool = False


@dataclass
class AppConfig:
    """Persistent application configuration."""

    backend: str = "ollama"  # Options: "ollama", "openai_compatible"
    base_url: str = "http://localhost:11434"
    api_key: str = ""
    model: str = "hermes3"
    theme: str = "dark"
    language: str = "en"
    default_system_prompt: str = (
        "You are Nous Hermes 3, a helpful, accurate, and steerables assistant."
    )
    generation: GenerationConfig = field(default_factory=GenerationConfig)


PRESETS: Dict[str, GenerationConfig] = {
    "code_analysis": GenerationConfig(
        temperature=0.2,
        top_p=0.85,
        max_tokens=4096,
        context_length=128000,
        repeat_penalty=1.05,
        json_mode=False,
    ),
    "creative_roleplay": GenerationConfig(
        temperature=0.85,
        top_p=0.95,
        max_tokens=3072,
        context_length=128000,
        repeat_penalty=1.1,
        json_mode=False,
    ),
    "precise_assistant": GenerationConfig(
        temperature=0.35,
        top_p=0.9,
        max_tokens=2048,
        context_length=128000,
        repeat_penalty=1.05,
        json_mode=False,
    ),
}


def init_workspace(workspace: Path = DEFAULT_WORKSPACE) -> Dict[str, Path]:
    """Create local directories for config, chat sessions, cache, and exports."""
    dirs = {
        "root": workspace,
        "sessions": workspace / "sessions",
        "exports": workspace / "exports",
        "cache": workspace / "cache",
    }
    for path in dirs.values():
        path.mkdir(parents=True, exist_ok=True)
    return dirs


def load_config(workspace: Path = DEFAULT_WORKSPACE) -> AppConfig:
    """Load configuration from disk or create default configuration on first run."""
    dirs = init_workspace(workspace)
    config_file = dirs["root"] / "config.json"

    if not config_file.exists():
        cfg = AppConfig()
        save_config(cfg, workspace)
        return cfg

    raw = json.loads(config_file.read_text(encoding="utf-8"))
    gen_data = raw.pop("generation", {})
    gen_cfg = GenerationConfig(**gen_data)
    return AppConfig(**raw, generation=gen_cfg)


def save_config(cfg: AppConfig, workspace: Path = DEFAULT_WORKSPACE) -> None:
    """Persist application configuration to JSON."""
    dirs = init_workspace(workspace)
    config_file = dirs["root"] / "config.json"
    payload: Dict[str, Any] = asdict(cfg)
    config_file.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
