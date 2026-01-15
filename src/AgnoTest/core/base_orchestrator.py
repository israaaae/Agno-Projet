# core/agent_os_factory.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence, Optional

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
    # Cache pour éviter les doubles builds
    _built_os: Optional[AgentOS] = field(default=None, init=False, repr=False)


    def with_interface(self, interface: BaseInterface) -> "AgentOSFactory":
        """Add interface from BaseInterface builder."""
        self.interfaces = list(self.interfaces) + [interface.build()]
        return self


    def build(self) -> AgentOS:
        # Retourne le cache si déjà construit
        if self._built_os is not None:
            return self._built_os
        try:
            kwargs = {
                k: v for k, v in {
                    "description": self.description,
                    "agents": list(self.agents) or None,
                    "teams": list(self.teams) or None,
                    "interfaces": list(self.interfaces) or None,
                    "tracing": self.tracing,
                }.items() if v
            }
            kwargs.update(self.extra)
            
            self._built_os = AgentOS(**kwargs)
            LOGGER.info("Built AgentOS OK")
            return self._built_os
        except Exception as e:
            LOGGER.exception("Failed to build AgentOS", extra={"error": str(e)})
            raise OrchestratorError(f"Failed to build AgentOS: {e}") from e

    def get_app(self):
        return self.build().get_app()

    def serve(self, app: str, reload: bool = False, host: str = "127.0.0.1", port: int = 2222):
        return self.build().serve(app=app, reload=reload, host=host, port=port)