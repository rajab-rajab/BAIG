from __future__ import annotations

import customtkinter as ctk

from src import theme


class TerminalPanel(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkBaseClass) -> None:
        super().__init__(master, fg_color=theme.SURFACE, corner_radius=6, border_width=1, border_color=theme.BORDER)
        ctk.CTkLabel(self, text="Embedded Execution Terminal", font=("Segoe UI Semibold", 15), text_color=theme.TEXT).pack(
            anchor="w", padx=14, pady=(12, 8)
        )
        self.output = ctk.CTkTextbox(self, fg_color=theme.OBSIDIAN, text_color=theme.TEXT, font=theme.MONO_FONT, wrap="word")
        self.output.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.output.tag_config("error", foreground=theme.RED)

    def append(self, text: str, is_error: bool = False) -> None:
        self.output.configure(state="normal")
        self.output.insert("end", text, "error" if is_error else None)
        self.output.see("end")
        self.output.configure(state="disabled")
