"""Runs generated project commands and streams their output without blocking the UI."""

from __future__ import annotations

import queue
import subprocess
import sys
import threading
from pathlib import Path


class TerminalRunner:
    def __init__(self, working_directory: Path) -> None:
        self.working_directory = working_directory
        self.events: queue.Queue[tuple[str, str | int]] = queue.Queue()

    def initialize(self) -> None:
        self._run([sys.executable, "main.py", "init"])

    def _run(self, command: list[str]) -> None:
        def worker() -> None:
            try:
                process = subprocess.Popen(
                    command,
                    cwd=self.working_directory,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding="utf-8",
                )
                assert process.stdout is not None
                assert process.stderr is not None
                for line in process.stdout:
                    self.events.put(("stdout", line))
                for line in process.stderr:
                    self.events.put(("stderr", line))
                self.events.put(("exit", process.wait()))
            except OSError as error:
                self.events.put(("stderr", f"Unable to run generated app: {error}\n"))
                self.events.put(("exit", 1))

        threading.Thread(target=worker, daemon=True).start()

    def drain_events(self) -> list[tuple[str, str | int]]:
        drained: list[tuple[str, str | int]] = []
        while True:
            try:
                drained.append(self.events.get_nowait())
            except queue.Empty:
                return drained
