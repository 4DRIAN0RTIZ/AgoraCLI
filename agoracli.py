import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils import Colors
from agora_sesion import AgoraSesion
from calificaciones_consultor import CalificacionesConsultor
import getpass
import sys

class AgoraCLI:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.sesion = AgoraSesion(self.driver)
        self.consultor = CalificacionesConsultor(self.driver)

    def ejecutar(self, usuario):
        try:
            contrasena = getpass.getpass(prompt="Contraseña: ")
            # Limpiar la última línea
            sys.stdout.write("\033[F")
            print("Iniciando sesión en Agora...")
            self.sesion.iniciar_sesion(usuario, contrasena)
            self.consultor.consultar_calificacion()
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            self.driver.quit()
            print("\n")
            print(Colors.colorize("Gracias por usar AgoraCLI", f"{Colors.BOLD}{Colors.BG_WHITE}{Colors.BLACK}"))
            github_profile = Colors.colorize("https://github.com/4DRIAN0RTIZ", Colors.GREEN)
            blog_site = Colors.colorize("https://cuevaneander.tech", Colors.GREEN)
            print(f"Github: {github_profile}")
            print(f"Blog: {blog_site}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Consulta calificaciones en Agora UTJ.')
    parser.add_argument('-m', '--matricula', type=str, required=True, help='Matrícula de estudiante')
    
    args = parser.parse_args()
    cli = AgoraCLI()
    cli.ejecutar(args.matricula)
