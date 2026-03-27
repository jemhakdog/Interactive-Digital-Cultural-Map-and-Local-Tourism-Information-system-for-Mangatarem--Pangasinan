$exeName = "AdminApp.exe"
$exePath = Join-Path $PSScriptRoot "..\" $exeName
# Also check dist folder as PyInstaller defaults there
$distPath = Join-Path $PSScriptRoot "..\dist" $exeName

if (Test-Path $distPath) {
    $exePath = $distPath
}

$shortcutPath = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\Startup\AdminApp.lnk"

if (Test-Path $exePath) {
    Write-Host "Found executable at $exePath"
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($shortcutPath)
    $Shortcut.TargetPath = $exePath
    $Shortcut.WorkingDirectory = Split-Path $exePath -Parent
    $Shortcut.Save()
    Write-Host "Auto-start shortcut created successfully at $shortcutPath"
} else {
    Write-Warning "Executable not found ($exeName). Please run Task 5 (Packaging) first."
    Write-Host "Note: This script expects the executable to be in the project root or 'dist' folder."
}
