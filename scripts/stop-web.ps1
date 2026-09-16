$ErrorActionPreference = "Stop"
$projectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$runtimeDir = Join-Path $projectRoot ".runtime"
$stateFile = Join-Path $runtimeDir "web-processes.json"
$stopped = [System.Collections.Generic.HashSet[int]]::new()

function Stop-OwnedProcess([int]$ProcessId) {
    if ($ProcessId -le 0 -or $stopped.Contains($ProcessId)) { return }
    $processInfo = Get-CimInstance Win32_Process -Filter "ProcessId=$ProcessId" -ErrorAction SilentlyContinue
    if (-not $processInfo) { return }
    $commandLine = [string]$processInfo.CommandLine
    $executable = [string]$processInfo.ExecutablePath
    if (-not ($commandLine.Contains($projectRoot) -or $executable.StartsWith($projectRoot))) {
        Write-Warning "PID $ProcessId was not stopped because it does not belong to this LabourLawyer directory."
        return
    }
    Stop-Process -Id $ProcessId -Force -ErrorAction SilentlyContinue
    [void]$stopped.Add($ProcessId)
}

if (Test-Path -LiteralPath $stateFile) {
    $state = Get-Content -LiteralPath $stateFile -Raw | ConvertFrom-Json
    if ($state.backendPid) { Stop-OwnedProcess ([int]$state.backendPid) }
    if ($state.frontendPid) { Stop-OwnedProcess ([int]$state.frontendPid) }
    if ($state.digitalHumanPid) { Stop-OwnedProcess ([int]$state.digitalHumanPid) }
}

foreach ($port in 8000, 5173, 3000) {
    $connections = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    foreach ($connection in $connections) {
        Stop-OwnedProcess ([int]$connection.OwningProcess)
    }
}

if (Test-Path -LiteralPath $stateFile) {
    Remove-Item -LiteralPath $stateFile -Force
}
Write-Host "LabourLawyer web processes have been stopped." -ForegroundColor Green
