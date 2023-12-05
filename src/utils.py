import sys
import shutil

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
