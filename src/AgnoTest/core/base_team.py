from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional, Sequence

from agno.team import Team
from ..utils.exceptions import TeamBuildError
from ..utils.logging import LOGGER


@dataclass
class BaseTeam:
    """Enveloppe légère autour de agno.team.Team."""

    name: str
    role: Optional[str] = None
    model: Any = None
    members: Sequence[Any] = field(default_factory=list)
    instructions: Optional[str | List[str]] = None
    extra: dict = field(default_factory=dict)

    def build(self) -> Team:
        try:
            kwargs = dict(
                name=self.name,
                role=self.role,
                model=self.model,
                members=list(self.members),
                instructions=self.instructions,
            )
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            kwargs.update(self.extra)
            team = Team(**kwargs)
            LOGGER.info("Built Team OK", extra={"team_name": self.name})
            return team
        except Exception as e:
            LOGGER.exception("Failed to build Team", extra={"team_name": self.name, "error": str(e)})
            raise TeamBuildError(f"Failed to build Team {self.name!r}: {e}") from e

