"""
utils.py
Copyleft (c) 2023 Oscar Adrian Ortiz Bustos

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

"""
import sys
import shutil
import platform
import os
from pathlib import Path

class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    INVERSE = '\033[7m'

    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

    @staticmethod
    def colorize(text, color):
        return f"{color}{text}{Colors.RESET}"


class Clear:
    @staticmethod
    def pantalla():
        terminal_width = shutil.get_terminal_size().columns
        print(" " * terminal_width, end="\r")
    @staticmethod
    # Borrar el 100% de la linea anterior
    def linea_anterior():
        print("\033[F\033[K", end="")

    @staticmethod
    # Borrar el 100% de una cantidad de lineas
    def lineas_anteriores(cantidad):
        for _ in range(cantidad):
            Clear.linea_anterior()

def get_download_path():
    """
    Returns the download path based on the operating system.
    """
    user_home = Path.home()
    if platform.system() == "Linux":
        download_path = f"{user_home}/Downloads/AgoraCLIFiles/"
    elif platform.system() == "Windows":
        download_path = f"{user_home}\\Downloads\\AgoraCLIFiles\\"
    elif platform.system() == "Darwin":  # Para macOS
        download_path = f"{user_home}/Downloads/AgoraCLIFiles/"
    else:
        raise Exception("S.O. no compatible. Reporta este problema especificando tu sistema operativo.")
    
    # Crea el directorio de descarga si no existe
    os.makedirs(download_path, exist_ok=True)

    # prefs
    prefs = {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True
    }
    
    return download_path, prefs

def goodbye_message():
    print("\n")
    print(Colors.colorize("Gracias por usar AgoraCLI", f"{Colors.BOLD}{Colors.BG_WHITE}{Colors.BLACK}"))
    github_profile = Colors.colorize("https://github.com/4DRIAN0RTIZ", Colors.GREEN)
    blog_site = Colors.colorize("https://neandertech.netlify.app/blog", Colors.GREEN)
    print(f"Github: {github_profile}")
    print(f"Blog: {blog_site}")
    sys.exit(0)
