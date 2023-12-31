#!/bin/bash

# This script is used to install AgoraCLI.
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
# install.sh
# Copyleft (c) 2023 Oscar Adrian Ortiz Bustos

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.


# Ansi color codes
red='\033[0;31m'
green='\033[0;32m'
yellow='\033[0;33m'
blue='\033[0;34m'
reset='\033[0m'

agoracli_path="$HOME/.local/bin/AgoraCLI" # Path to install AgoraCLI
# Check if the path doesnt exist
if [ ! -d "$agoracli_path" ]; then
	echo -e "${red}El directorio $agoracli_path no existe.${reset}"
	echo -e "${yellow}Creando directorio $agoracli_path...${reset}"
	mkdir -p "$agoracli_path" # Create the directory
	echo -e "${green}Directorio $agoracli_path creado.${reset}"
fi

virtual_env_name="AgoraCLI"
virtual_env_path="$agoracli_path/$virtual_env_name"

function ctrl_c() {
	echo -e "\n${red}Instalación cancelada por el usuario (CTRL + C).${reset}"
	exit 1
}

trap ctrl_c INT

function get_distro() {
	distro=$(grep -m1 "^ID=" /etc/os-release | awk -F'=' '{print $2}' | tr -d '"')
	distro_like=$(grep -m1 "^ID_LIKE=" /etc/os-release | awk -F'=' '{print $2}' | tr -d '"')

	case "$distro" in
	"debian" | "ubuntu" | "linuxmint" | "kali")
		echo "apt"
		;;
	"fedora" | "centos" | "rhel")
		echo "dnf"
		;;
	"arch" | "manjaro" | *arch*)
		echo "pacman"
		;;
	*)
		if [[ $distro_like == *arch* ]]; then
			echo "pacman"
		else
		echo "No se pudo determinar el gestor de paquetes.\nPor favor, instala los siguientes paquetes manualmente:\npython3\npython3-pip\npython3-venv\nwget"
		fi
		;;
	esac
}

package_handler=$(get_distro)

declare -A dependencies=(
	["python3"]="sudo $package_handler install python-is-python3"
	["pip"]="sudo $package_handler install python3-pip"
	["venv"]="sudo $package_handler install python3-venv"
	["wget"]="sudo $package_handler install wget"
)

for dependency in "${!dependencies[@]}"; do
	if ! command -v "$dependency" &>/dev/null; then
		echo -e "${yellow}Instalando $dependency...${reset}"
		eval "${dependencies[$dependency]}" # Install the dependency
		if [ $? -ne 0 ]; then
			echo -e "${red}No se pudo instalar $dependency.${reset}"
			exit 1
		fi
		echo -e "${green}$dependency instalado.${reset}"
	fi
done

cd "$agoracli_path" || exit # Change directory to $HOME/.local/bin/agoracli. If the directory doesnt exist, exit the script.
declare -A files_to_download=(
	["agoracli.py"]="https://raw.githubusercontent.com/4DRIAN0RTIZ/AgoraCLI/master/src/agoracli.py"
	["agora_sesion.py"]="https://raw.githubusercontent.com/4DRIAN0RTIZ/AgoraCLI/master/src/agora_sesion.py"
	["calificaciones_consultor.py"]="https://raw.githubusercontent.com/4DRIAN0RTIZ/AgoraCLI/master/src/calificaciones_consultor.py"
	["utils.py"]="https://raw.githubusercontent.com/4DRIAN0RTIZ/AgoraCLI/master/src/utils.py"
	["requirements.txt"]="https://raw.githubusercontent.com/4DRIAN0RTIZ/AgoraCLI/master/requirements.txt"
	["adeudo_consultor.py"]="https://raw.githubusercontent.com/4DRIAN0RTIZ/AgoraCLI/master/src/adeudo_consultor.py"
	["horario_consultor.py"]="https://raw.githubusercontent.com/4DRIAN0RTIZ/AgoraCLI/master/src/horario_consultor.py"
)

for file in "${!files_to_download[@]}"; do
	echo -e "${yellow}Descargando $file...${reset}"
	wget -q "${files_to_download[$file]}" -O "$file" # Download the file
	# Give execute permissions to the file
	chmod +x "$file"
done

echo -e "${green}Descarga completada.${reset}"
echo -e "${yellow}Creando entorno virtual...${reset}"
python3 -m venv "$virtual_env_name" # Create a virtual environment
echo -e "${green}Entorno virtual creado.${reset}"
echo -e "${yellow}Activando entorno virtual...${reset}"
source "$virtual_env_path/bin/activate"
echo -e "${green}Entorno virtual activado.${reset}"
echo -e "${yellow}Instalando dependencias...${reset}"
pip install -r requirements.txt # Install dependencies from requirements.txt
echo -e "${green}Dependencias instaladas.${reset}"
echo -e "${yellow}Desactivando entorno virtual...${reset}"
deactivate # Deactivate the virtual environment
echo -e "${green}Entorno virtual desactivado.${reset}"
echo -e "${blue}Creando script de activación...${reset}"
# Create a bash script to activate the virtual environment, run AgoraCLI and deactivate the virtual environment.
echo -e "#!/bin/bash\nsource $virtual_env_path/bin/activate\npython3 $agoracli_path/agoracli.py \"\$@\"\ndeactivate" >agoracli.sh
chmod +x agoracli.sh # Make the bash script executable
echo -e "${green}Script de activación creado.${reset}"
echo -e "${blue}Creando enlace simbólico...${reset}"
# If symlink exists, omit the creation of the symlink
if [ -L "$HOME/.local/bin/agoracli" ]; then
	rm "$HOME/.local/bin/agoracli" # Remove the symlink
fi
ln -s "$agoracli_path/agoracli.sh" "$HOME/.local/bin/agoracli" # Create a symbolic link to the bash script
echo "---"
echo -e "${green}Instalación completada.${reset}"
echo -e "${yellow}Uso:${reset} ${blue}agoracli -m <matricula> -c | -a | -ho${reset}"
echo -e "${yellow}Ayuda:${reset} ${blue}agoracli -h${reset}"
echo -e "${green}AgoraCLI es software libre. Copyleft (c) 2023 Oscar Adrian Ortiz Bustos. Licencia GPLv3.${reset}"
