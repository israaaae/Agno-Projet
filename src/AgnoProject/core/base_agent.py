from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Sequence
from agno.agent import Agent

from .config import SETTINGS
from ..utils.exceptions import AgentBuildError
from ..utils.logging import LOGGER


def _default_model():
    provider = SETTINGS.DEFAULT_MODEL_PROVIDER
    model_id = SETTINGS.DEFAULT_MODEL_ID

    if provider == "openai":
        from agno.models.openai import OpenAIChat

        return OpenAIChat(id=model_id)
    if provider == "google":
        from agno.models.google import Gemini  # type: ignore

        return Gemini(id=model_id)
    return None


@dataclass
class BaseAgent:
    """Enveloppe stable Agno Agent."""

    name: str
    role: Optional[str] = None
    instructions: Optional[str | list[str]] = None
    model: Any = None
    tools: Sequence[Callable[..., Any] | Any] = field(default_factory=list)
    markdown: bool = SETTINGS.MARKDOWN

    extra: dict = field(default_factory=dict)

    def build(self) -> Agent:

        try:
            model = self.model or _default_model()
            kwargs = dict(
                name=self.name,
                model=model,
                role=self.role,
                tools=self.tools,
                instructions=self.instructions,
            )
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            kwargs.update(self.extra)

            agent = Agent(**kwargs)
            LOGGER.info("Built Agent OK", extra={"agent_name": self.name})
            return agent
        except Exception as e:
            LOGGER.exception("Failed to build Agent", extra={"agent_name": self.name, "error": str(e)})
            raise AgentBuildError(f"Failed to build Agent {self.name!r}: {e}") from e

