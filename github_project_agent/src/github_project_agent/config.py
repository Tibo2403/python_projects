from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    openai_model: str
    workspace: Path
    github_token: str | None

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        workspace = Path(os.getenv("AGENT_WORKSPACE", ".agent-workspace")).resolve()
        return cls(
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            workspace=workspace,
            github_token=os.getenv("GITHUB_TOKEN") or None,
        )

