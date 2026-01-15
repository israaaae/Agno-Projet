from __future__ import annotations

import os
from typing import Literal

from pydantic import BaseModel, Field


class Settings(BaseModel):
    ENV: Literal["dev", "test", "prod"] = Field(default="dev")
    DEBUG: bool = Field(default=True)
    SQLITE_DB_FILE: str = Field(default="data/agents.db")

    DEFAULT_MODEL_PROVIDER: Literal["openai", "anthropic", "google", "custom"] = Field(default="openai")
    DEFAULT_MODEL_ID: str = Field(default="gpt-4o-mini")
    MARKDOWN: bool = Field(default=True)

    AGENT_OS_DESCRIPTION: str = Field(default="AgentOS (Agno)")
    ENABLE_TRACING: bool = Field(default=True)

    @staticmethod
    def load(prefix: str = "") -> "Settings":
        env = os.environ
        data = {}

        def get_bool(key: str, default: bool) -> bool:
            v = env.get(prefix + key)
            if v is None:
                return default
            return v.strip().lower() in {"1", "true", "yes", "y", "on"}

        def get_str(key: str, default: str) -> str:
            return env.get(prefix + key, default)

        data["ENV"] = get_str("ENV", "dev")
        data["DEBUG"] = get_bool("DEBUG", True)

        data["DEFAULT_MODEL_PROVIDER"] = get_str("DEFAULT_MODEL_PROVIDER", "openai")
        data["DEFAULT_MODEL_ID"] = get_str("DEFAULT_MODEL_ID", "gpt-4o-mini")

        data["AGENT_OS_DESCRIPTION"] = get_str("AGENT_OS_DESCRIPTION", "AgentOS (Agno)")
        data["ENABLE_TRACING"] = get_bool("ENABLE_TRACING", False)

        return Settings(**data)

SETTINGS = Settings.load()

