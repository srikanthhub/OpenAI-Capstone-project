# Run this script as Administrator

Write-Output "Starting Disk Cleanup..."

# 1. Clear Windows Temp Folder
$tempWin = "$env:windir\Temp"
Remove-Item "$tempWin\*" -Recurse -Force -ErrorAction SilentlyContinue
Write-Output "Cleared Windows Temp: $tempWin"

# 2. Clear User Temp Folder
$tempUser = "$env:LOCALAPPDATA\Temp"
Remove-Item "$tempUser\*" -Recurse -Force -ErrorAction SilentlyContinue
Write-Output "Cleared User Temp: $tempUser"

# 3. Clear Prefetch Files
$prefetch = "$env:windir\Prefetch"
Remove-Item "$prefetch\*" -Recurse -Force -ErrorAction SilentlyContinue
Write-Output "Cleared Prefetch Folder: $prefetch"

# 4. Clear SoftwareDistribution\Download (Windows Update files)
$updateDownload = "$env:windir\SoftwareDistribution\Download"
Remove-Item "$updateDownload\*" -Recurse -Force -ErrorAction SilentlyContinue
Write-Output "Cleared Windows Update Downloads: $updateDownload"

# 5. Clear Recycle Bin
Write-Output "Emptying Recycle Bin..."
Clear-RecycleBin -Force -ErrorAction SilentlyContinue

# 6. Clear Windows.old folder if it exists
$winOld = "$env:SystemDrive\Windows.old"
if (Test-Path $winOld) {
    Remove-Item "$winOld" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Output "Removed Windows.old folder: $winOld"
} else {
    Write-Output "No Windows.old folder found"
}

# 7. Clear Microsoft Store Cache
$storeCache = "$env:LOCALAPPDATA\Packages\Microsoft.WindowsStore"
if (Test-Path "$storeCache") {
    Get-ChildItem -Path "$storeCache" -Recurse -Force -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -like "*LocalCache*" } |
    Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
    Write-Output "Cleared Microsoft Store Cache"
}

Write-Output "✅ Disk Cleanup Completed!"
