import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils import Colors
from agora_sesion import AgoraSesion
from calificaciones_consultor import CalificacionesConsultor
from adeudo_consultor import AdeudoConsultor
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
        self.adeudo_consultor = AdeudoConsultor(self.driver)

    def iniciar_sesion(self, usuario):
        try:
            contrasena = getpass.getpass(prompt="Contraseña: ")
            sys.stdout.write("\033[F")
            print("Iniciando sesión en Agora...")
            self.sesion.iniciar_sesion(usuario, contrasena)
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)
     
    def consultar_calificaciones(self):
        self.consultor.consultar_calificacion()

    def consultar_adeudo(self):
        self.adeudo_consultor.consultar_adeudo()

    def ejecutar(self, usuario, args):
        self.iniciar_sesion(usuario)

        if args.calificaciones:
            self.consultar_calificaciones()
        if args.adeudo:
            self.consultar_adeudo()
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
    parser.add_argument('-a', '--adeudo', action='store_true', help='Muestra adeudo de estudiante')
    parser.add_argument('-c', '--calificaciones', action='store_true', help='Muestra calificaciones de estudiante')
    args = parser.parse_args()
    cli = AgoraCLI()
    cli.ejecutar(args.matricula, args)
