from __future__ import annotations
from dataclasses import dataclass
from ..core.base_interface import BaseInterface
from ..utils.logging import LOGGER
from ..utils.exceptions import InterfaceBuildError

@dataclass
class WhatsappInterface(BaseInterface):
    """WhatsApp interface builder."""

    def build(self):
        from agno.os.interfaces.whatsapp import Whatsapp
        
        try:
            kwargs = dict(
                agent=self.agent,
                team=self.team,
            )
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            kwargs.update(self.extra)
            
            interface = Whatsapp(**kwargs)
            LOGGER.info("Built WhatsApp interface OK")
            return interface
        except Exception as e:
            LOGGER.exception("Failed to build WhatsApp interface", extra={"error": str(e)})
            raise InterfaceBuildError(f"Failed to build WhatsApp interface: {e}") from e

