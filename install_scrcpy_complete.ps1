Write-Host "Installing complete scrcpy package for Windows..." -ForegroundColor Green
Write-Host ""

# Create temp directory
$tempDir = "temp"
if (!(Test-Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir | Out-Null
}

Set-Location $tempDir

try {
    # Get latest release info
    Write-Host "Getting latest scrcpy version..." -ForegroundColor Yellow
    $response = Invoke-WebRequest -Uri "https://api.github.com/repos/Genymobile/scrcpy/releases/latest" -UseBasicParsing
    $latest = $response.Content | ConvertFrom-Json
    
    # Find Windows 64-bit zip
    $win64Asset = $latest.assets | Where-Object { $_.name -like "*win64*.zip" } | Select-Object -First 1
    
    if (!$win64Asset) {
        throw "Could not find Windows 64-bit release"
    }
    
    $downloadUrl = $win64Asset.browser_download_url
    Write-Host "Downloading: $($win64Asset.name)" -ForegroundColor Yellow
    
    # Download scrcpy
    Invoke-WebRequest -Uri $downloadUrl -OutFile "scrcpy.zip"
    
    if (!(Test-Path "scrcpy.zip")) {
        throw "Failed to download scrcpy"
    }
    
    # Extract scrcpy
    Write-Host "Extracting scrcpy..." -ForegroundColor Yellow
    Expand-Archive -Path "scrcpy.zip" -DestinationPath "." -Force
    
    # Find extracted directory
    $extractedDir = Get-ChildItem -Directory -Name "scrcpy-win64-*" | Select-Object -First 1
    
    if (!$extractedDir) {
        throw "Could not find extracted scrcpy directory"
    }
    
    Write-Host "Found extracted directory: $extractedDir" -ForegroundColor Yellow
    
    # Copy all files from extracted directory to parent directory
    Write-Host "Installing scrcpy files..." -ForegroundColor Yellow
    Copy-Item "$extractedDir\*" "..\" -Recurse -Force
    
    # Clean up
    Set-Location ..
    Remove-Item $tempDir -Recurse -Force
    
    Write-Host ""
    Write-Host "Complete scrcpy installation finished!" -ForegroundColor Green
    Write-Host "You can now run: python phone_mirror.py" -ForegroundColor Cyan
    Write-Host ""
    
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Manual installation:" -ForegroundColor Yellow
    Write-Host "1. Go to https://github.com/Genymobile/scrcpy/releases" -ForegroundColor White
    Write-Host "2. Download the latest scrcpy-win64-*.zip" -ForegroundColor White
    Write-Host "3. Extract ALL files to this directory (not just scrcpy.exe)" -ForegroundColor White
    Write-Host ""
}

Read-Host "Press Enter to continue" 