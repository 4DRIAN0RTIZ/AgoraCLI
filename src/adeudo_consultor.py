"""
adeudo_consultor.py
Copyleft (c) 2023 Oscar Adrian Ortiz Bustos

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

"""
import time
import tabulate
from selenium.webdriver.common.by import By
import platform
import shutil
import pandas as pd
import os
import sys
from utils import Clear
from utils import Colors
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AdeudoConsultor:
    def __init__(self, driver, download_path):
        self.driver = driver
        self.download_path = download_path

    def consultar_adeudo(self):
        Clear.pantalla()
        print("Consultando adeudo...")
        self.driver.get("https://agora.utj.edu.mx/adeudo/adeudo")
        try:
            # Esperar a que el div con id "Totales" sea visible
            totales_div = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "men"))
            )
            # Obtener el valor del div "Totales"
            total_adeudo_text = totales_div.text
            if total_adeudo_text.startswith("Usted debe"):
                # Continuar a Finanzas -> Referencias
                self.driver.get("https://agora.utj.edu.mx/Finanzas/referencias")
                element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#trv-main-menu-export-command > .k-link"))
                )
                time.sleep(2)
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
                options_div = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "k-animation-container"))
                )
                time.sleep(2)
                export_list = options_div.find_element(By.ID, "trv-main-menu-export-format-list")
                export_option = export_list.find_element(By.CSS_SELECTOR, "[data-command-parameter='XLSX']")
                export_option.click()
                self.esperar_descarga()
                # Open file
                self.procesar_referencias()
            else:
                # Mostrar mensaje "Sin Adeudo" con bordes en ASCII
                print("+" + "-"*12 + "+")
                print("| Sin Adeudo |")
                print("+" + "-"*12 + "+")
        except Exception as e:
            print("Error: No se pudo obtener las referencias bancarias del alumno.", e)
            sys.exit(1)
 
    def esperar_descarga(self):
        # Elimina archivos anteriores
        files = os.listdir(self.download_path)
        for file in files:
            if file.startswith("Referencia") and file.endswith(".xlsx"):
                os.remove(os.path.join(self.download_path, file))

        # Esperar hasta que un nuevo archivo se descargue
        while True:
            files = os.listdir(self.download_path)
            horario_files = [f for f in files if f.startswith("Referencia") and f.endswith(".xlsx")]
            if horario_files:
                time.sleep(1)  # Asegurar que la descarga esté completamente finalizada
                break

    def open_file(self):
        files = os.listdir(self.download_path)
        horario_files = [f for f in files if f.startswith("Referencia") and f.endswith(".xlsx")]

        if not horario_files:
            print("Error: No se encontró ningún archivo de horario.")
            sys.exit(1)

        # Seleccionar el archivo más reciente
        latest_file = max(horario_files, key=lambda f: os.path.getmtime(os.path.join(self.download_path, f)))

        # Confirmar que solo se procese el archivo más reciente
        for file in horario_files:
            if file != latest_file:
                os.remove(os.path.join(self.download_path, file))

        return os.path.join(self.download_path, latest_file)
    

    def procesar_referencias(self):
        Clear.linea_anterior()
        file_path = self.open_file()
        if file_path is None:
            print("Error: No se pudo encontrar el archivo de las referencias.")
            sys.exit(1)
        Clear.linea_anterior()
        df = pd.read_excel(file_path, header=None)

        matricula = df.loc[5,1].strip()
        nombreAlumno = df.loc[5, 5].strip()
        carrera = df.loc[5, 17].strip()
        cep = df.loc[6, 17].strip()
        banco = df.loc[6, 1].strip()
        concepto1 = df.loc[9, 0].strip()
        concepto2 = df.loc[13, 0].strip()
        concepto3 = df.loc[17, 0].strip()
        importe1 = df.loc[9, 3]
        importe2 = df.loc[13, 3]
        importe3 = df.loc[17, 3]
        referencia1 = df.loc[10, 5].strip()
        referencia2 = df.loc[14, 5].strip()
        referencia3 = df.loc[18, 5].strip()
        total = importe1 + importe2 + importe3

        print("\nNombre: {}".format(nombreAlumno))
        print("Matricula: {}".format(matricula))
        print("Carrera: {}".format(carrera))
        print("CEP: {}".format(cep))
        print("Concepto: {}".format(concepto1))

        table_data = []

        table_headers = ["Concepto", "Importe", "Referencia"]
        colalign = ["center", "center", "center"]
        table_data.append([concepto1, importe1, referencia1])
        table_data.append([concepto2, importe2, referencia2])
        table_data.append([concepto3, importe3, referencia3])
        table_data.append(["Total", total, ""])
        self.tabla_referencias = tabulate.tabulate(table_data, headers=table_headers, tablefmt="grid", colalign=colalign)
        Clear.linea_anterior()
        print(Colors.colorize("Recuerda pagar en el banco: {}".format(banco), Colors.GREEN))
        print(self.tabla_referencias)
