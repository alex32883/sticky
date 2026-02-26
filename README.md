# Sticky Notes

A modern, lightweight sticky notes application for Windows Desktop built with Python and PyQt6.

## Features

- **Dashboard:** Main window displaying all sticky notes in a responsive grid
- **Create Note:** Floating action button (+) to add new notes
- **Note Card Design:**
  - Editable title and content
  - Task list with checkboxes (strikethrough when completed)
  - Color picker (Yellow, Pink, Blue, Green, Purple)
  - Delete button per note
- **Data Persistence:** Notes saved automatically to `%AppData%\StickyNotes\notes.json`
- **Window:** Resizable, centered on startup, optional minimize to system tray

## Tech Stack

- **Language:** Python 3.8+
- **Framework:** tkinter (built-in with Python)
- **Storage:** Local JSON file
- **Architecture:** MVVM (Model-View-ViewModel)

## Project Structure

```
sticky/
├── main.py              # Application entry point
├── models/              # Data models
│   ├── note.py          # Note model
│   └── task_item.py     # TaskItem model
├── viewmodels/          # MVVM logic
│   └── main_viewmodel.py
├── views/               # UI components
│   ├── main_window.py   # Dashboard window
│   └── note_card.py     # Sticky note card widget
├── services/            # Storage & services
│   └── storage.py       # JSON persistence
├── requirements.txt
└── README.md
```

## How to Run

### Option 1: Run with Python (no pip install required)

```powershell
python main.py
```

### Option 2: Build Windows executable

To create a `.exe` you can double-click to run:

1. Install build dependency (one-time):
   ```powershell
   pip install pyinstaller
   ```

2. Build the executable:
   ```powershell
   python -m PyInstaller --onefile --windowed --name "Sticky Notes" main.py
   ```

   Or double-click `build.bat` for a one-step build.

3. The executable will be at: `dist\Sticky Notes.exe`

   Copy it anywhere and run by double-clicking. Notes are still saved to `%AppData%\StickyNotes\notes.json`.
   The exe uses a book-shaped icon (created by `make_icon.py`). If Pillow is installed, a nicer icon is generated; otherwise a minimal icon is used.

## Notes Data Location

Notes are stored at: `%APPDATA%\StickyNotes\notes.json`

You can back up or restore notes by copying this file.

## Git & GitHub

Git is configured for this project with:

- **Identity:** `user.name` and `user.email` set globally (GitHub noreply email).
- **Credentials:** Credential helper set to `manager` (Windows). On first `git push`, you’ll be prompted to sign in to GitHub.
- **Remote:** `origin` → `https://github.com/alex32883/sticky.git`
- **Branch:** `main` tracks `origin/main`.

**First-time push:**

1. Create the repository on GitHub: [github.com/new](https://github.com/new) → name it `sticky`, leave it empty.
2. Push: `git push -u origin main`
3. When prompted, sign in with your GitHub account. Use a **Personal Access Token (PAT)** as the password, not your GitHub password: [Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens) → Generate new token (classic), scope `repo`.

After that, the credential manager will remember your token for future pushes and pulls.
