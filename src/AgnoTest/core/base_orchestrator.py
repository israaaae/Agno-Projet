# core/agent_os_factory.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from agno.os import AgentOS
from agno.os.interfaces.whatsapp import Whatsapp

from .config import SETTINGS
from ..utils.exceptions import OrchestratorError
from ..utils.logging import LOGGER

# core/agent_os_factory.py - Usage
from .base_interface import BaseInterface

@dataclass
class AgentOSFactory:
    """Builder AgentOS (FastAPI)."""

    agents: Sequence[Any] = field(default_factory=list)
    teams: Sequence[Any] = field(default_factory=list)
    workflows: Sequence[Any] = field(default_factory=list)
    interfaces: Sequence[Any] = field(default_factory=list)  # Add interfaces
    description: str = SETTINGS.AGENT_OS_DESCRIPTION
    tracing: bool = SETTINGS.ENABLE_TRACING

    extra: dict = field(default_factory=dict)


    def with_interface(self, interface: BaseInterface) -> "AgentOSFactory":
        """Add interface from BaseInterface builder."""
        self.interfaces = list(self.interfaces) + [interface.build()]
        return self


    def build(self) -> AgentOS:
        try:
            kwargs = dict(
                description=self.description,
                agents=list(self.agents) if self.agents else None,
                teams=list(self.teams) if self.teams else None,
                interfaces=list(self.interfaces) if self.interfaces else None,
                tracing=self.tracing,  # Enables traceability

            )
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            kwargs.update(self.extra)
            os_obj = AgentOS(**kwargs)
            LOGGER.info("Built AgentOS OK")
            return os_obj
        except Exception as e:
            LOGGER.exception("Failed to build AgentOS", extra={"error": str(e)})
            raise OrchestratorError(f"Failed to build AgentOS: {e}") from e

    def get_app(self):
        return self.build().get_app()

    def serve(self, app: str, reload: bool = False, host: str = "127.0.0.1", port: int = 2222):
        return self.build().serve(app=app, reload=reload, host=host, port=port)