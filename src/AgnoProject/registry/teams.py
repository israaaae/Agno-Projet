from .agents import AGENTS
from ..teams import review_contract

def build_teams():
    team = review_contract(
        members=[
            AGENTS["structure"],
            AGENTS["legal"],
            AGENTS["negotiation"],
        ]
    )
    return {"review_contract": team}

TEAMS = build_teams()
