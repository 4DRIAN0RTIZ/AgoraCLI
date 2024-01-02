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
import shutil
from utils import Clear

class AdeudoConsultor:
    def __init__(self, driver):
        self.driver = driver

    def consultar_adeudo(self):
        Clear.pantalla()
        print("Consultando adeudo...")
        self.driver.get("https://agora.utj.edu.mx/adeudo/adeudo")
        time.sleep(2)
        # Limpia la consola con shutil
        terminal_width = shutil.get_terminal_size().columns
        print(" " * terminal_width, end="\r")
        table_data = []
        adeudo_div = self.driver.find_element(By.ID, "Totales")
        adeudo_text = adeudo_div.find_element(By.ID, "men")
        adeudo = adeudo_text.text
        table_data.append([adeudo])
        table_headers = ["Adeudo"]
        colalign = ["center"]
        salida = tabulate.tabulate(table_data, headers=table_headers, tablefmt="grid", colalign=colalign)
        Clear.linea_anterior()
        print(salida)
