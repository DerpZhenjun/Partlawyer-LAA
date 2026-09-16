param(
    [switch]$NoBrowser,
    [switch]$WithDigitalHuman
)

$ErrorActionPreference = "Stop"
$projectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$backendDir = Join-Path $projectRoot "backend"
$frontendDir = Join-Path $projectRoot "frontend"
$digitalHumanDir = Join-Path $projectRoot "ChatVRM"
$runtimeDir = Join-Path $projectRoot ".runtime"
$venvDir = Join-Path $projectRoot ".venv"
$pythonExe = Join-Path $venvDir "Scripts\python.exe"
$requirements = Join-Path $backendDir "requirements-api.txt"
$stateFile = Join-Path $runtimeDir "web-processes.json"

New-Item -ItemType Directory -Force -Path $runtimeDir | Out-Null

function Test-HttpUrl([string]$Url) {
    try {
        $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2
        return $response.StatusCode -ge 200 -and $response.StatusCode -lt 500
    } catch {
        return $false
    }
}

function Wait-HttpUrl([string]$Url, [string]$ServiceName, [int]$Seconds = 45) {
    for ($index = 0; $index -lt $Seconds; $index++) {
        if (Test-HttpUrl $Url) {
            Write-Host "[OK] $ServiceName is ready." -ForegroundColor Green
            return
        }
        Start-Sleep -Seconds 1
    }
    throw "$ServiceName startup timed out. Check logs in $runtimeDir."
}

if (-not (Test-Path -LiteralPath $pythonExe)) {
    Write-Host "[1/4] Creating the backend environment..." -ForegroundColor Cyan
    $uvCommand = Get-Command uv -ErrorAction SilentlyContinue
    if ($uvCommand) {
        & $uvCommand.Source venv $venvDir --python 3.11
    } else {
        $pyCommand = Get-Command py -ErrorAction SilentlyContinue
        if (-not $pyCommand) {
            throw "Python and uv are both unavailable. Install Python 3.11+ or uv from https://docs.astral.sh/uv/."
        }
        & $pyCommand.Source -3.11 -m venv $venvDir
    }
}

$previousErrorPreference = $ErrorActionPreference
$ErrorActionPreference = "SilentlyContinue"
& $pythonExe -c "import fastapi, uvicorn, docx, litellm" 2>$null
$dependencyCheckExitCode = $LASTEXITCODE
$ErrorActionPreference = $previousErrorPreference
if ($dependencyCheckExitCode -ne 0) {
    Write-Host "[2/4] Installing backend dependencies (first run only)..." -ForegroundColor Cyan
    $uvCommand = Get-Command uv -ErrorAction SilentlyContinue
    if ($uvCommand) {
        & $uvCommand.Source pip install --python $pythonExe -r $requirements
    } else {
        & $pythonExe -m pip install -r $requirements
    }
}

$npmCommand = Get-Command npm.cmd -ErrorAction SilentlyContinue
if (-not $npmCommand) {
    throw "Node.js/npm was not found. Install Node.js 20 or newer."
}

if (-not $env:LABOURLAWYER_LLM_MODEL) {
    try {
        $ollamaModels = @((Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 3).models.name)
        $modelPreference = @("qwen3.5:4b", "qwen3.5:9b", "qwen3.5:2b", "qwen3.5:27b", "qwen3.5:0.8b")
        $selectedModel = $modelPreference | Where-Object { $ollamaModels -contains $_ } | Select-Object -First 1
        if (-not $selectedModel) {
            $selectedModel = $ollamaModels | Where-Object { $_ -match "qwen|deepseek" } | Select-Object -First 1
        }
        if ($selectedModel) {
            $env:LABOURLAWYER_LLM_MODEL = "ollama/$selectedModel"
            Write-Host "[OK] AI model: $selectedModel" -ForegroundColor Green
        } else {
            Write-Host "[WARN] No local AI model found. Run: ollama pull qwen3.5:4b" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "[WARN] Ollama is not running. Documents still work; start Ollama to use the AI advisor." -ForegroundColor Yellow
    }
}

if (-not (Test-Path -LiteralPath (Join-Path $frontendDir "node_modules"))) {
    Write-Host "[3/4] Installing frontend dependencies..." -ForegroundColor Cyan
    & $npmCommand.Source install --prefix $frontendDir
    if ($LASTEXITCODE -ne 0) { throw "Frontend dependency installation failed." }
}

$state = [ordered]@{
    startedAt = (Get-Date).ToString("o")
    backendPid = $null
    frontendPid = $null
    digitalHumanPid = $null
}

if (Test-HttpUrl "http://127.0.0.1:8000/health") {
    Write-Host "[OK] Backend is already running." -ForegroundColor Green
} else {
    Write-Host "[4/4] Starting backend..." -ForegroundColor Cyan
    $backendProcess = Start-Process -FilePath $pythonExe `
        -ArgumentList @("-m", "uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000") `
        -WorkingDirectory $backendDir -WindowStyle Hidden -PassThru `
        -RedirectStandardOutput (Join-Path $runtimeDir "backend.log") `
        -RedirectStandardError (Join-Path $runtimeDir "backend-error.log")
    $state.backendPid = $backendProcess.Id
}

if (Test-HttpUrl "http://127.0.0.1:5173") {
    Write-Host "[OK] Frontend is already running." -ForegroundColor Green
} else {
    Write-Host "[4/4] Starting frontend..." -ForegroundColor Cyan
    $frontendProcess = Start-Process -FilePath $npmCommand.Source `
        -ArgumentList @("run", "dev", "--", "--host", "127.0.0.1", "--port", "5173", "--strictPort") `
        -WorkingDirectory $frontendDir -WindowStyle Hidden -PassThru `
        -RedirectStandardOutput (Join-Path $runtimeDir "frontend.log") `
        -RedirectStandardError (Join-Path $runtimeDir "frontend-error.log")
    $state.frontendPid = $frontendProcess.Id
}

if ($WithDigitalHuman) {
    if (-not (Test-Path -LiteralPath (Join-Path $digitalHumanDir "node_modules"))) {
        Write-Host "Installing digital-human dependencies (first run only)..." -ForegroundColor Cyan
        & $npmCommand.Source install --prefix $digitalHumanDir --legacy-peer-deps
        if ($LASTEXITCODE -ne 0) { throw "Digital-human dependency installation failed." }
    }
    if (Test-HttpUrl "http://127.0.0.1:3000") {
        Write-Host "[OK] Digital human is already running." -ForegroundColor Green
    } else {
        Write-Host "Starting digital human..." -ForegroundColor Cyan
        $digitalHumanProcess = Start-Process -FilePath $npmCommand.Source `
            -ArgumentList @("run", "dev", "--", "-H", "127.0.0.1", "-p", "3000") `
            -WorkingDirectory $digitalHumanDir -WindowStyle Hidden -PassThru `
            -RedirectStandardOutput (Join-Path $runtimeDir "digital-human.log") `
            -RedirectStandardError (Join-Path $runtimeDir "digital-human-error.log")
        $state.digitalHumanPid = $digitalHumanProcess.Id
    }
}

$state | ConvertTo-Json | Set-Content -LiteralPath $stateFile -Encoding UTF8
Wait-HttpUrl "http://127.0.0.1:8000/health" "Backend"
Wait-HttpUrl "http://127.0.0.1:5173" "Frontend"
if ($WithDigitalHuman) {
    Wait-HttpUrl "http://127.0.0.1:3000" "Digital human" 90
}

Write-Host ""
Write-Host "LabourLawyer is ready:" -ForegroundColor Green
Write-Host "  Web:  http://127.0.0.1:5173"
Write-Host "  API:  http://127.0.0.1:8000/docs"
if ($WithDigitalHuman) { Write-Host "  Digital human: http://127.0.0.1:3000" }
Write-Host "  Logs: $runtimeDir"
Write-Host "  Stop: double-click stop-web.bat"

if (-not $NoBrowser) {
    Start-Process "http://127.0.0.1:5173"
}
