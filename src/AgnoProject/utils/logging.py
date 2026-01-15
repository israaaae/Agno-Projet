from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from .paths import PATHS


def setup_logging(
    name: str = "app",
    level: int | None = None,
    log_file: Path | None = None,
    max_bytes: int = 5_000_000,
    backup_count: int = 3,
) -> logging.Logger:
    logger = logging.getLogger(name)
    if getattr(logger, "_configured", False):
        return logger

    logger.setLevel(level or logging.INFO)
    logger.propagate = False

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    file_path = log_file or (PATHS.logs_dir / f"{name}.log")
    fh = RotatingFileHandler(file_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    logger._configured = True  # type: ignore[attr-defined]
    return logger


LOGGER = setup_logging("agentos")

