"""
agoracli.py
Copyleft (c) 2023 Oscar Adrian Ortiz Bustos

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

"""
import platform
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils import Colors, get_download_path, show_goodbye_message
from agora_sesion import AgoraSesion
from calificaciones_consultor import CalificacionesConsultor
from adeudo_consultor import AdeudoConsultor
from horario_consultor import HorarioConsultor
import getpass
import sys
import os

class AgoraCLI:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")
        download_path, prefs = get_download_path()
        chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.sesion = AgoraSesion(self.driver)
        self.consultor = CalificacionesConsultor(self.driver)
        self.adeudo_consultor = AdeudoConsultor(self.driver, download_path)
        self.horario_consultor = HorarioConsultor(self.driver, download_path)

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

    def consultar_horario(self):
        self.horario_consultor.consultar_horario()

    def ejecutar(self, usuario, args):
        self.iniciar_sesion(usuario)

        if args.calificaciones:
            self.consultar_calificaciones()
        if args.adeudo:
            self.consultar_adeudo()
        if args.horario:
            self.consultar_horario()
        self.driver.quit()

        show_goodbye_message()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Consulta calificaciones en Agora UTJ.')
    parser.add_argument('-m', '--matricula', type=str, required=True, help='Matrícula de estudiante')
    parser.add_argument('-a', '--adeudo', action='store_true', help='Muestra adeudo de estudiante y las referencias para pagar')
    parser.add_argument('-c', '--calificaciones', action='store_true', help='Muestra calificaciones de estudiante')
    parser.add_argument('-ho', '--horario', action='store_true', help='Muestra horario de estudiante')
    args = parser.parse_args()
    cli = AgoraCLI()
    cli.ejecutar(args.matricula, args)
