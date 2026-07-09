# Steam Download Manager PRO 🎮

A smart, lightweight GUI tool specifically designed for Game Centers and PC cafes to easily block and unblock Steam Workshop and background game downloads, preventing unwanted data usage and bandwidth drain.

<p align="center">
  <img src="icon.png" width="150" alt="Logo">
</p>

## 🌟 Features
- **Block/Unblock Workshop Downloads:** Stop automatic mod and map updates that consume high bandwidth.
- **Block/Unblock All Game Updates:** Prevent games from updating in the background while still allowing already installed games to run normally.
- **Smart Status Detection:** Live monitoring of directory permissions indicating if downloads are currently `Blocked 🔴` or `Active 🟢`.
- **Premium GUI:** Built with `customtkinter` for a modern, dark-themed user interface.
- **Portable & Fast-Loading:** One-click execution without the need for extraction delays.

## 🚀 How It Works
The application works by modifying the Windows directory permissions (`icacls`) for specific Steam folders:
- `steamapps/workshop/downloads`
- `steamapps/downloading`

By denying write permissions (`W,WD,AD`), Steam is physically prevented from downloading updates, effectively saving data.

## 🛠️ Installation & Build
To build the `.exe` file from the source code, simply run:
```bat
build_exe.bat
```
This will:
1. Install necessary Python dependencies (`customtkinter`, `pyinstaller`, `Pillow`).
2. Convert `icon.png` to an `.ico` file.
3. Build the application using PyInstaller for instant loading speed.
4. Output the ready-to-use software in the `dist/Steam_Manager_Pro` directory.

## 📖 Usage
1. Open `Steam_Manager_Pro.exe` as **Administrator**.
2. Verify or browse for your Steam library path.
3. Click **Block** to stop downloads, or **Unblock** to resume normal Steam behavior.

## ⚠️ Notes for Developers
- Ensure the application is run with Administrator privileges, otherwise the `icacls` commands will throw a `PermissionError`.
- If the icon fails to apply in Windows Explorer, it is due to the Windows icon cache. The current build script circumvents this by generating a fresh output directory.
