# app_telegram.py
from __future__ import annotations

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

# Make `import AgnoTest...` work with src-layout when running `uvicorn app_telegram:app`.
SRC = ROOT / "src"
if SRC.exists() and str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from src.AgnoTest.core.base_orchestrator import AgentOSFactory  # noqa: E402
from src.AgnoTest.interfaces.telegram import TelegramInterface  # noqa: E402
from src.AgnoTest.registry.teams import TEAMS  # noqa: E402

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")  # optional (fallback)

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("Set TELEGRAM_BOT_TOKEN (in .env or env vars).")

agent_os = (
    # AgentOS requires at least one of: agents/teams
    AgentOSFactory(teams=[TEAMS["review_contract"]])
    .with_interface(
        TelegramInterface(
            token=TELEGRAM_BOT_TOKEN,
            chat_id=TELEGRAM_CHAT_ID,
            team=TEAMS["review_contract"],
        )
    )
    .build()
)

# ASGI app for uvicorn
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="app_telegram:app", port=8000, reload=True)