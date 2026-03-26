$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$venvPyInstaller = Join-Path $projectRoot ".venv\Scripts\pyinstaller.exe"
$installerScript = Join-Path $projectRoot "installer\AUREXA_BOREAL.iss"

if (-not (Test-Path $venvPython)) {
    throw "Python da .venv nao encontrado. Rode primeiro .\setup_venv.ps1"
}

if (-not (Test-Path $venvPyInstaller)) {
    throw "PyInstaller nao encontrado na .venv. Rode primeiro .\setup_venv.ps1"
}

Write-Host "Limpando build anterior..."
Remove-Item -LiteralPath (Join-Path $projectRoot "build") -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath (Join-Path $projectRoot "dist") -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath (Join-Path $projectRoot "installer_output") -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Gerando executavel com PyInstaller..."
& $venvPyInstaller (Join-Path $projectRoot "app_main.spec")

if (-not (Test-Path (Join-Path $projectRoot "dist\AUREXA_BOREAL.exe"))) {
    throw "Executavel nao foi gerado em dist\\AUREXA_BOREAL.exe"
}

$iscc = Get-Command iscc -ErrorAction SilentlyContinue
if (-not $iscc) {
    Write-Warning "Inno Setup Compiler (iscc) nao encontrado."
    Write-Warning "Instale o Inno Setup e depois rode: iscc `"$installerScript`""
    exit 0
}

Write-Host "Gerando instalador com Inno Setup..."
& $iscc.Source $installerScript

Write-Host "Build finalizado."
