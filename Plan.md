# Role
Act as a Senior Windows Desktop Developer and UI/UX Designer.

# Objective
Create a modern, lightweight Sticky Notes application for Windows Desktop. The application should be visually appealing, intuitive, and functional.

# Tech Stack
- **Language:** python
- **Framework:** PyQt (or latest stable)

- **Data Storage:** Local JSON file for persistence (save notes between sessions)
- **Architecture:** MVVM (Model-View-ViewModel) pattern

# Core Features
1. **Dashboard:** A main window that displays all active sticky notes in a grid or wrap panel layout.
2. **Create Note:** A button to add a new note.
3. **Note Card Design:**
   - Each note should look like a physical sticky note.
   - **Title:** Editable text field at the top.
   - **Content:** Editable text area.
   - **Task List:** Ability to add checklist items within a note. Each item must have a checkbox to mark it as completed (strikethrough text when checked).
   - **Color Picker:** A small button on each note to cycle through or select different background colors (e.g., Yellow, Pink, Blue, Green, Purple).
   - **Delete:** A close/delete button on each note.
4. **Data Persistence:** All notes, their colors, text, and checklist states must be saved automatically to a local `notes.json` file and loaded on startup.
5. **Window Behavior:**
   - The main window should be resizable.
   - Minimize to System Tray (optional but preferred).
   - Start with the window centered on the screen.

# UI/UX Requirements
- **Aesthetic:** Clean, flat design with subtle shadows (elevation) to make notes pop.
- **Typography:** Use a clean sans-serif font (e.g., Segoe UI or Roboto).
- **Interactions:** Smooth hover effects on buttons. The "Add Note" button should be prominent (Floating Action Button style).
- **Responsiveness:** Notes should reflow automatically when the main window is resized.

# Implementation Steps
1. **Setup:** Provide the necessary NuGet package references (MaterialDesignThemes, Newtonsoft.Json or System.Text.Json).
2. **Models:** Create the `Note` and `TaskItem` classes with properties for ID, Title, Content, Color, and List of Tasks.
3. **ViewModel:** Create a `MainViewModel` to handle the logic for adding, deleting, saving, and loading notes. Implement `INotifyPropertyChanged`.
4. **Views:**
   - `MainWindow.xaml`: The container for the notes.
   - `NoteCardControl.xaml`: A reusable User Control for the individual sticky note design.
5. **Styling:** Define the color palette in `App.xaml` or a Resource Dictionary.
6. **Logic:** Implement the JSON serialization/deserialization logic to save state to `%AppData%`.

# Deliverables
- Provide the full project structure.
- Provide the code for all critical files (Models, ViewModels, XAML Views, App.xaml).
- Include instructions on how to run the project in Visual Studio.
- Ensure the code is commented and clean.