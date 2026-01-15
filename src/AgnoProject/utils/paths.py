from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    root: Path
    data_dir: Path
    logs_dir: Path

    @staticmethod
    def detect(root: Path | None = None) -> "ProjectPaths":
        r = (root or Path.cwd()).resolve()
        data_dir = r / "data"
        logs_dir = r / "logs"
        data_dir.mkdir(parents=True, exist_ok=True)
        logs_dir.mkdir(parents=True, exist_ok=True)
        return ProjectPaths(root=r, data_dir=data_dir, logs_dir=logs_dir)


PATHS = ProjectPaths.detect()

