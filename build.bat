@echo off
REM Build Sticky Notes Windows executable
echo Closing Sticky Notes if running...
taskkill /IM "Sticky Notes.exe" /F 2>nul

echo Removing old build...
if exist "dist\Sticky Notes.exe" del /F /Q "dist\Sticky Notes.exe" 2>nul
if exist "dist\Sticky Notes.exe" (
    echo ERROR: Cannot delete dist\Sticky Notes.exe - close it and try again.
    pause
    exit /b 1
)

echo Installing PyInstaller...
python -m pip install pyinstaller --quiet

echo.
echo Creating icon (book shape)...
python make_icon.py

echo.
echo Building executable...
if exist icon.ico (
    python -m PyInstaller --onefile --windowed --name "Sticky Notes" --icon=icon.ico --clean --noconfirm main.py
) else (
    python -m PyInstaller --onefile --windowed --name "Sticky Notes" --clean --noconfirm main.py
)

echo.
if exist "dist\Sticky Notes.exe" (
    echo SUCCESS! Executable created at: dist\Sticky Notes.exe
    echo You can copy it anywhere and run by double-clicking.
) else (
    echo Build may have failed. Check output above.
)
pause
