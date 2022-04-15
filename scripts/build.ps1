$curr_path = Get-Location
$app_path = Split-Path -Parent ${PSScriptRoot}

Set-Location $app_path

Invoke-Expression -Command .\scripts\cleanup.ps1

python .\setup.py build

Set-Location $curr_path