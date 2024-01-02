# This script is used to install AgoraCLI using PowerShell.
#
# Author: 4DRI4N0RTIZ (NeanderTech)
# Date: 2023-12-03
#
#       __                     _          _____  __ ___          _____           _        _ _
#    /\ \ \___  __ _ _ __   __| | ___ _ _/__   \/__/ __\/\  /\   \_   \_ __  ___| |_ __ _| | |
#   /  \/ / _ \/ _` | '_ \ / _` |/ _ | '__|/ /\/_\/ /  / /_/ /    / /\| '_ \/ __| __/ _` | | |
#  / /\  |  __| (_| | | | | (_| |  __| |  / / //_/ /__/ __  /  /\/ /_ | | | \__ | || (_| | | |
#  \_\ \/ \___|\__,_|_| |_|\__,_|\___|_|  \/  \__\____\/ /_/   \____/ |_| |_|___/\__\__,_|_|_|
#
# install.ps1
# Copyleft (c) 2023 Oscar Adrian Ortiz Bustos

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

$agoracli_path = "$env:USERPROFILE\.config\AgoraCLI" # Path to install AgoraCLI
# Check if the path doesn't exist
if (-not (Test-Path $agoracli_path -PathType Container)) {
    Write-Host "El directorio $agoracli_path no existe."
    Write-Host "Creando directorio $agoracli_path..."
    New-Item -ItemType Directory -Path $agoracli_path | Out-Null # Create the directory
    Write-Host "Directorio $agoracli_path creado."
}

$virtual_env_name = "AgoraCLI"
$virtual_env_path = Join-Path $agoracli_path $virtual_env_name

$files_to_download = @{
    "agoracli.py" = "https://raw.githubusercontent.com/4DRIAN0RTIZ/AgoraCLI/master/src/agoracli.py"
    "agora_sesion.py" = "https://raw.githubusercontent.com/4DRIAN0RTIZ/AgoraCLI/master/src/agora_sesion.py"
    "calificaciones_consultor.py" = "https://raw.githubusercontent.com/4DRIAN0RTIZ/AgoraCLI/master/src/calificaciones_consultor.py"
    "utils.py" = "https://raw.githubusercontent.com/4DRIAN0RTIZ/AgoraCLI/master/src/utils.py"
    "requirements.txt" = "https://raw.githubusercontent.com/4DRIAN0RTIZ/AgoraCLI/master/requirements.txt"
    "adeudo_consultor.py" = "https://raw.githubusercontent.com/4DRIAN0RTIZ/AgoraCLI/master/src/adeudo_consultor.py"
    "horario_consultor.py" = "https://raw.githubusercontent.com/4DRIAN0RTIZ/AgoraCLI/master/src/horario_consultor.py"
    "agoracli.bat" = "https://gist.githubusercontent.com/4DRIAN0RTIZ/859c8354e41d629d9bc1329ba5878363/raw/2a65e6d822ffb49ba49e874090c6c62a880afd40/agoracli.bat"
}

foreach ($file in $files_to_download.Keys) {
    $fullPath = Join-Path $agoracli_path $file
    Write-Host "Descargando $file..."
    (New-Object System.Net.WebClient).DownloadFile($files_to_download[$file], $fullPath) # Download the file
    # Give execute permissions to the file (assuming it's a script)
    if ($file -match '\.py$') {
        # Optionally, you can add execute permissions for the user
        # Add-Content -Path $fullPath -Value "`r`n# Your PowerShell Script Here"
    }
}

Write-Host "Descarga completada."
Write-Host "Creando entorno virtual..."
Set-Location -Path $agoracli_path -ErrorAction Stop # Change directory to $HOME/.local/bin/agoracli. If the directory doesn't exist, exit the script.
python -m venv $virtual_env_name # Create a virtual environment
Write-Host "Entorno virtual creado."
Write-Host "Activando entorno virtual..."
& "$virtual_env_path\Scripts\Activate" # Activate the virtual environment
Write-Host "Entorno virtual activado."
Write-Host "Actualizando pip en el entorno virtual..."
& "$virtual_env_path\Scripts\python.exe" -m pip install --upgrade pip
Write-Host "Pip actualizado en el entorno virtual."
Write-Host "Instalando dependencias..."
& "$virtual_env_path\Scripts\pip" install -r "$agoracli_path\requirements.txt" # Install dependencies from requirements.txt
Write-Host "Dependencias instaladas."
Write-Host "Desactivando entorno virtual..."
& "$virtual_env_path\Scripts\Deactivate" # Deactivate the virtual environment
Write-Host "Entorno virtual desactivado."
# ...

Write-Host "Agregando al PATH de Windows..."
$existingPath = [System.Environment]::GetEnvironmentVariable('Path', [System.EnvironmentVariableTarget]::User)
$newPath = "$existingPath;$($agoracli_path)"
[System.Environment]::SetEnvironmentVariable('Path', $newPath, [System.EnvironmentVariableTarget]::User)
# Crear un acceso directo llamado "agoracli" en el mismo directorio que agoracli.bat
$shortcutPath = [System.IO.Path]::Combine($agoracli_path, 'agoracli.lnk')
$targetPath = [System.IO.Path]::Combine($agoracli_path, 'agoracli.bat')

# Creamos un objeto para el acceso directo
$WScriptShell = New-Object -ComObject WScript.Shell
$shortcut = $WScriptShell.CreateShortcut($shortcutPath)

# Asignamos la ruta al archivo .bat al acceso directo
$shortcut.TargetPath = $targetPath

# Guardamos el acceso directo
$shortcut.Save()
Write-Host "---"
Write-Host "Instalación completada."
Write-Host "---"
Write-Host "Uso: agoracli -m <matricula> | -c | -a | -ho"
Write-Host "Ayuda: agoracli -h"
Write-Host "AgoraCLI es software libre. Copyleft (c) 2023 Oscar Adrian Ortiz Bustos, bajo licencia GPL v3."

