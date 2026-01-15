from __future__ import annotations
from typing import Any, Sequence
from ..core.base_team import BaseTeam
from ..core.config import SETTINGS
from textwrap import dedent
def _team_model():
    if SETTINGS.DEFAULT_MODEL_PROVIDER == "openai":
        from agno.models.openai import OpenAIChat
        return OpenAIChat(id=SETTINGS.DEFAULT_MODEL_ID)
    if SETTINGS.DEFAULT_MODEL_PROVIDER == "google":
        from agno.models.google import Gemini  # type: ignore
        return Gemini(id=SETTINGS.DEFAULT_MODEL_ID)
    return None

def review_contract(*, members: Sequence[Any]):
    return BaseTeam(
        name="review_contract_team",
        role="Contract structure + legal framework + negociation expert",
        model=_team_model(),
        members=list(members),
        instructions=dedent("""
        You are the lead summarizer.
        You must combine input from:
        1. Legal Agent
        2. Structure Agent
        3. Negotiation Agent

        Key Requirements:
        - Ensure traceability: every insight must be backed by a quoted clause.
        - Organize the final output into clear sections:
          • Legal Analysis
          • Structural Review
          • Negotiation Opportunities
        - Avoid duplication.
        - Produce a final, decision-ready report.
        """),
        # Note: `agno.team.Team` only accepts a limited set of kwargs; keep extras minimal.
        extra={
            "markdown": True,
        },
    ).build()


