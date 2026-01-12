from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional, Sequence
from abc import ABC, abstractmethod
from agno.agent import Agent
from agno.team import Team

@dataclass
class BaseInterface(ABC):
    """Base class for interface builders."""
    
    agent: Optional[Agent] = None
    team: Optional[Team] = None
    extra: dict = field(default_factory=dict)

    @abstractmethod
    def build(self) -> Any:
        pass
