"""
Sticky Notes - A modern, lightweight desktop sticky notes application.
Uses tkinter (built-in) - no pip install required.
"""

import sys
import tkinter as tk
from tkinter import font as tkfont

from viewmodels.main_viewmodel import MainViewModel
from views.main_window import MainWindow


def main() -> None:
    viewmodel = MainViewModel()
    window = MainWindow(viewmodel)
    default_font = tkfont.nametofont("TkDefaultFont")
    default_font.configure(family="Segoe UI", size=10)
    window.run()

    sys.exit(0)


if __name__ == "__main__":
    main()
