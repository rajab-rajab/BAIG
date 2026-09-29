"""Coordinates the offline BuildTrace project generation flow."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from src.fallback_provider import FallbackProvider
from src.payload_validator import validate_payload
from src.project_writer import ProjectWriter
from src.terminal_runner import TerminalRunner

ProgressCallback = Callable[[str, str], None]
FilesCallback = Callable[[dict[str, Path]], None]


class BuildController:
    def __init__(
        self,
        progress_callback: ProgressCallback,
        files_callback: FilesCallback,
        fallback_provider: FallbackProvider | None = None,
        project_writer: ProjectWriter | None = None,
    ) -> None:
        self.progress_callback = progress_callback
        self.files_callback = files_callback
        self.fallback_provider = fallback_provider or FallbackProvider()
        self.project_writer = project_writer or ProjectWriter()
        self.terminal_runner: TerminalRunner | None = None

    def build_offline(self) -> TerminalRunner:
        self.progress_callback("database.py", "active")
        payload = validate_payload(self.fallback_provider.load())
        self.progress_callback("database.py", "complete")
        self.progress_callback("main.py", "active")
        self.progress_callback("main.py", "complete")
        self.progress_callback("README.md", "active")
        self.progress_callback("README.md", "complete")
        self.progress_callback("disk_write", "active")
        files = self.project_writer.write(payload)
        self.files_callback(files)
        self.progress_callback("disk_write", "complete")
        self.progress_callback("auto_execution", "active")
        self.terminal_runner = TerminalRunner(self.project_writer.output_dir)
        self.terminal_runner.initialize()
        return self.terminal_runner
