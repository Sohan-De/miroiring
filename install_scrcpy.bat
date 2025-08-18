@echo off
echo Installing scrcpy for Windows...
echo.

REM Create temp directory
if not exist "temp" mkdir temp
cd temp

REM Get the latest scrcpy version
echo Getting latest scrcpy version...
powershell -Command "& {$response = Invoke-WebRequest -Uri 'https://api.github.com/repos/Genymobile/scrcpy/releases/latest' -UseBasicParsing; $latest = $response.Content | ConvertFrom-Json; $assets = $latest.assets | Where-Object {$_.name -like '*win64*.zip'}; if ($assets) { $assets[0].browser_download_url } else { 'https://github.com/Genymobile/scrcpy/releases/latest/download/scrcpy-win64.zip' }}"

REM Download scrcpy (latest version)
echo Downloading scrcpy...
powershell -Command "& {try { $response = Invoke-WebRequest -Uri 'https://api.github.com/repos/Genymobile/scrcpy/releases/latest' -UseBasicParsing; $latest = $response.Content | ConvertFrom-Json; $assets = $latest.assets | Where-Object {$_.name -like '*win64*.zip'}; if ($assets) { $url = $assets[0].browser_download_url; Write-Host 'Downloading:' $url; Invoke-WebRequest -Uri $url -OutFile 'scrcpy.zip' } else { Write-Host 'Downloading fallback version...'; Invoke-WebRequest -Uri 'https://github.com/Genymobile/scrcpy/releases/latest/download/scrcpy-win64.zip' -OutFile 'scrcpy.zip' }} catch { Write-Host 'Error downloading scrcpy. Please check your internet connection.'; exit 1 }}"

if not exist "scrcpy.zip" (
    echo Failed to download scrcpy. Please check your internet connection.
    echo.
    echo Manual installation:
    echo 1. Go to https://github.com/Genymobile/scrcpy/releases
    echo 2. Download the latest scrcpy-win64-*.zip
    echo 3. Extract and copy scrcpy.exe to this directory
    pause
    exit /b 1
)

REM Extract scrcpy
echo Extracting scrcpy...
powershell -Command "& {Expand-Archive -Path 'scrcpy.zip' -DestinationPath '.' -Force}"

REM Find the extracted folder
for /d %%i in (scrcpy-win64-*) do set SCRCPY_DIR=%%i

if not defined SCRCPY_DIR (
    echo Could not find extracted scrcpy directory.
    echo Please manually extract scrcpy.zip and copy scrcpy.exe to the parent directory.
    pause
    exit /b 1
)

REM Copy scrcpy.exe to current directory
echo Installing scrcpy...
copy "%SCRCPY_DIR%\scrcpy.exe" "..\scrcpy.exe"

REM Clean up
cd ..
rmdir /s /q temp

echo.
echo scrcpy installation complete!
echo You can now run: python phone_mirror.py
echo.
pause 