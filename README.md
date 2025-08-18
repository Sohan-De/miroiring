# Minimal Phone Mirror

A clean, focused script that mirrors and controls your Android phone via ADB using scrcpy. No extra UI, no interface, no design elements - just pure mirroring and control.

## Prerequisites

### 1. Install ADB (Android Debug Bridge)
Download and install Android SDK Platform Tools:
- **Windows**: Download from [Android Developer](https://developer.android.com/studio/releases/platform-tools)
- **macOS**: `brew install android-platform-tools`
- **Linux**: `sudo apt install android-tools-adb`

### 2. Install scrcpy
Download scrcpy from the official repository:
- **Windows**: Download from [scrcpy releases](https://github.com/Genymobile/scrcpy/releases)
- **macOS**: `brew install scrcpy`
- **Linux**: `sudo apt install scrcpy`

### 3. Enable USB Debugging on Your Phone
1. Go to **Settings** → **About phone**
2. Tap **Build number** 7 times to enable Developer options
3. Go to **Settings** → **Developer options**
4. Enable **USB debugging**
5. Connect your phone via USB
6. Allow USB debugging when prompted on your phone

## Usage

### Option 1: Run with Python
```bash
python phone_mirror.py
```

### Option 2: Run with batch file (Windows)
Double-click `run_mirror.bat`

## Features

- **Automatic device detection**: Finds connected Android devices
- **Multiple device support**: Choose from multiple connected devices
- **Clean mirroring**: 60 FPS, 8Mbps bitrate, 1920px max width
- **No audio**: Keeps it minimal and focused
- **Easy control**: Use mouse and keyboard to control your phone
- **Clean exit**: Press Ctrl+C to stop mirroring

## Controls

Once mirroring starts, you can:
- **Click**: Tap on screen
- **Drag**: Scroll
- **Right-click**: Back button
- **Middle-click**: Home button
- **Ctrl+Shift+O**: Power button
- **Ctrl+Shift+M**: Menu button
- **Ctrl+Shift+W**: Volume up
- **Ctrl+Shift+S**: Volume down

## Troubleshooting

### "ADB not found"
- Make sure Android SDK Platform Tools is installed
- Add ADB to your system PATH

### "scrcpy not found"
- Download scrcpy from the official repository
- Add scrcpy to your system PATH

### "No Android devices found"
- Enable USB debugging on your phone
- Connect via USB cable
- Allow USB debugging when prompted
- Try a different USB cable or port

### Mirroring doesn't start
- Check that your phone is unlocked
- Ensure USB debugging is enabled
- Try disconnecting and reconnecting your phone

## Requirements

- Python 3.6+
- ADB (Android Debug Bridge)
- scrcpy
- Android phone with USB debugging enabled

## License

This script is provided as-is for personal use. 