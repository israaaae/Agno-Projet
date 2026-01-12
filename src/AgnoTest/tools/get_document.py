from io import BytesIO
from pathlib import Path


def get_document(*, files=None, text=None) -> str:
    if text:
        return text
    f = next(iter(files or ()), None)
    if not f:
        raise ValueError("No PDF provided.")

    raw = Path(getattr(f, "filepath")).read_bytes() if getattr(f, "filepath", None) else bytes(getattr(f, "content"))
    from pypdf import PdfReader  # type: ignore

    return "\n".join((p.extract_text() or "") for p in PdfReader(BytesIO(raw)).pages).strip()

