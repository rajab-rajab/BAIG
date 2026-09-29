"""The CustomTkinter shell that binds offline generation to visible UI panels."""

from __future__ import annotations

import customtkinter as ctk

from src import theme
from src.build_controller import BuildController
from src.ui.build_input_panel import BuildInputPanel
from src.ui.file_inspector import FileInspector
from src.ui.header_status import HeaderStatus
from src.ui.progress_tracker import ProgressTracker
from src.ui.terminal_panel import TerminalPanel


class BuildTraceApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.title("BuildTrace")
        self.geometry("1250x780")
        self.minsize(1024, 680)
        self.configure(fg_color=theme.BACKGROUND)
        self.grid_columnconfigure(0, weight=3, uniform="columns")
        self.grid_columnconfigure(1, weight=7, uniform="columns")
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.header = HeaderStatus(self)
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(16, 10))
        self.progress = ProgressTracker(self)
        self.progress.grid(row=1, column=1, sticky="new", padx=(6, 16), pady=(0, 6))
        self.inspector = FileInspector(self)
        self.inspector.grid(row=2, column=1, sticky="nsew", padx=(6, 16), pady=6)
        self.terminal = TerminalPanel(self, self.run_terminal_command)
        self.terminal.grid(row=3, column=1, sticky="nsew", padx=(6, 16), pady=(6, 16))
        self.input_panel = BuildInputPanel(self, self.start_offline_build)
        self.input_panel.grid(row=1, column=0, rowspan=3, sticky="nsew", padx=(16, 6), pady=(0, 16))
        self.controller = BuildController(self.on_progress, self.inspector.show_files)

    def on_progress(self, step: str, status: str) -> None:
        self.progress.set_status(step, status)

    def start_offline_build(self) -> None:
        self.input_panel.set_building(True)
        self.terminal.append("[offline] Loading the verified local template…\n")
        try:
            self.controller.build_offline()
            self.after(100, self.poll_terminal)
        except Exception as error:  # visible build error instead of a silent GUI failure
            self.on_progress("disk_write", "failed")
            self.terminal.append(f"Build failed: {error}\n", is_error=True)
            self.input_panel.set_building(False)

    def run_terminal_command(self, command: str) -> None:
        runner = self.controller.terminal_runner
        if runner is None:
            self.terminal.append("Build the offline project before running commands.\n", is_error=True)
            return
        self.terminal.append(f"> {command}\n")
        runner.run_demo_command(command)
        self.after(100, self.poll_terminal)

    def poll_terminal(self) -> None:
        runner = self.controller.terminal_runner
        if runner is None:
            return
        still_running = True
        for stream, value in runner.drain_events():
            if stream == "exit":
                exit_code = int(value)
                if exit_code == 0:
                    self.on_progress("auto_execution", "complete")
                    self.terminal.append("[verified] Generated project initialized successfully.\n")
                else:
                    self.on_progress("auto_execution", "failed")
                    self.terminal.append(f"[failed] Generated project exited with code {exit_code}.\n", is_error=True)
                self.input_panel.set_building(False)
                still_running = False
            else:
                self.terminal.append(str(value), is_error=stream == "stderr")
        if still_running:
            self.after(100, self.poll_terminal)
