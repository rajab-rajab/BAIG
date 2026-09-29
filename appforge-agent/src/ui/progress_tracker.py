from __future__ import annotations

import customtkinter as ctk

from src import theme


LABELS = {
    "database.py": "1. Generate database.py",
    "main.py": "2. Generate main.py",
    "README.md": "3. Generate README.md",
    "disk_write": "4. Disk Write Check",
    "auto_execution": "5. Auto-Execution",
}


class ProgressTracker(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkBaseClass) -> None:
        super().__init__(master, fg_color=theme.SURFACE, corner_radius=6, border_width=1, border_color=theme.BORDER)
        ctk.CTkLabel(self, text="Live Build Progress", font=("Segoe UI Semibold", 15), text_color=theme.TEXT).pack(
            anchor="w", padx=14, pady=(12, 8)
        )
        self.steps: dict[str, ctk.CTkLabel] = {}
        for key, label in LABELS.items():
            step = ctk.CTkLabel(self, text=f"○  {label}", anchor="w", font=theme.UI_FONT, text_color=theme.MUTED)
            step.pack(fill="x", padx=14, pady=3)
            self.steps[key] = step

    def set_status(self, key: str, status: str) -> None:
        icon, color = {
            "pending": ("○", theme.MUTED),
            "active": ("◉", theme.AMBER),
            "complete": ("●", theme.EMERALD),
            "failed": ("✕", theme.RED),
        }[status]
        self.steps[key].configure(text=f"{icon}  {LABELS[key]}", text_color=color)
