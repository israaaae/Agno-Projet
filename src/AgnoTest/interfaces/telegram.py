# interfaces/telegram.py
from dataclasses import dataclass
from typing import Optional

from agno.media import File
from agno.os.interfaces.base import BaseInterface as AgnoBaseInterface

from ..core.base_interface import BaseInterface
from ..utils.logging import LOGGER

# had la class TelegramOSInterface drnaha 7it Agno n'a pas d'interface telegram officielle comme Whatsapp 
# Donc on doit creer notre propre interface telegram

class TelegramOSInterface(AgnoBaseInterface):
    type: str = "telegram"
    prefix: str = "/telegram"
    tags = ["Telegram"]

    def __init__(self, *, token: str, chat_id: Optional[str] = None, agent=None, team=None):
        self.token = token
        self.chat_id = chat_id  # optional fallback
        self.agent = agent
        self.team = team

    def get_router(self, use_async: bool = True, **kwargs):
        from fastapi import APIRouter, Request
        from agno.tools.telegram import TelegramTools
        import httpx
        import tempfile
        from pathlib import Path

        router = APIRouter(prefix=self.prefix, tags=self.tags)
        agent = self.agent
        team = self.team
        runner = team or agent 

        @router.post("/webhook")
        async def telegram_webhook(request: Request):
            data = await request.json()
            message = data.get("message", {})
            text = message.get("text", "")
            incoming_chat_id = str(message.get("chat", {}).get("id") or "")
            reply_chat_id = incoming_chat_id or (str(self.chat_id) if self.chat_id is not None else "")
            telegram = TelegramTools(chat_id=reply_chat_id, token=self.token)

            # Handle file uploads (documents/PDFs)
            document = message.get("document")
            if document and runner is not None:
                file_id = document["file_id"]
                file_name = document.get("file_name", "document.pdf")
                suffix = Path(file_name).suffix or ".pdf"

                # Download file via Telegram API
                file_url = f"https://api.telegram.org/bot{self.token}/getFile?file_id={file_id}"
                async with httpx.AsyncClient() as client:
                    resp = await client.get(file_url)
                    tg_path = resp.json()["result"]["file_path"]
                    file_bytes = await client.get(f"https://api.telegram.org/file/bot{self.token}/{tg_path}")

                # Save to temp file and pass as Agno File(filepath=...)
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(file_bytes.content)
                    tmp_path = tmp.name

                response = runner.run(text or "Review this document.", files=[File(filepath=tmp_path, name=file_name)])
            elif runner is not None:
                response = runner.run(text)
            else:
                response = "No agent/team configured."

            telegram.send_message(str(getattr(response, "content", response)))
            return {"ok": True}

        self.router = router
        return router

# Voila hadi hiya la class b7al lli kayna f whatsapp.py 
# lfar9 juste que à la place de TelegramOSInterface il y a function whatsapp que Agno nous a fournit

@dataclass
class TelegramInterface(BaseInterface):
    """Telegram interface builder that returns an Agno-compatible OS interface."""

    token: Optional[str] = None
    chat_id: Optional[str] = None

    def build(self):
        if not self.token:
            raise ValueError("TelegramInterface requires `token`.")

        interface = TelegramOSInterface(token=self.token, chat_id=self.chat_id, agent=self.agent, team=self.team)
        LOGGER.info("Built Telegram interface OK")
        return interface
