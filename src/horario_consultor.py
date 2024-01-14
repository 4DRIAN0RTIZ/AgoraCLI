"""
horario_consultor.py
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
import tabulate
import sys
import os
import re
import pandas as pd
import time  # Importar el módulo time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import Clear

class HorarioConsultor:
    def __init__(self, driver):
        self.driver = driver
        if platform.system() == "Linux":
            home = "/home/{}".format(os.getlogin())
            self.download_path = "{}/Downloads/AgoraCLIFiles/".format(home)
        elif platform.system() == "Windows":
            home = "C:\\Users\\{}".format(os.getlogin())
            self.download_path = "{}\\Downloads\\AgoraCLIFiles\\".format(home)
        else:
            raise Exception("Parece que tu S.O. no es compatible con AgoraCLI.\nPor favor, abre un issue en el repositorio de Github mencionando tu S.O.")



    def obtener_nombre_materia(self):
        self.driver.get("https://agora.utj.edu.mx/consultaCalificacion/index")
        comboMateriasBtn = self.driver.find_element(By.ID, "comboMaterias")
        options = comboMateriasBtn.find_elements(By.TAG_NAME, "option")
        materias = []
        for option in options:
            materia = option.text
            if materia != "Selecciona...":
                materias.append(materia)
        return materias

    def consultar_horario(self):
        Clear.pantalla()
        print("Obteniendo horario del alumno...")
        self.driver.get("https://agora.utj.edu.mx/HorarioAlumno/ReporteHorarioAlumno")
        try:
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
            self.procesar_horario()
        except Exception as e:
            print("Error: No se pudo obtener el horario del alumno.", e)
            sys.exit(1)

    def esperar_descarga(self):
        while True:
            files = os.listdir(self.download_path)
            horario_files = [f for f in files if f.startswith("Horario") and f.endswith(".xlsx")]
            if horario_files:
                break
            time.sleep(1)

    def open_file(self):
        files = os.listdir(self.download_path)
        horario_files = [f for f in files if f.startswith("Horario") and f.endswith(".xlsx")]

        latest_file = None
        latest_time = 0
        for file in horario_files:
            file_path = os.path.join(self.download_path, file)
            file_time = os.path.getmtime(file_path)
            if file_time > latest_time:
                latest_time = file_time
                latest_file = file

        for file in horario_files:
            if file != latest_file:
                os.remove(os.path.join(self.download_path, file))

        if latest_file:
            return os.path.join(self.download_path, latest_file)
        return None


    def procesar_horario(self):
        file_path = self.open_file()
        if file_path is None:
            print("Error: No se pudo encontrar el archivo del horario.")
            sys.exit(1)
        Clear.linea_anterior()
        df = pd.read_excel(file_path, header=None)
        nombreAlumno = df.loc[8, 5].split(":")[-1].strip()
        situacionAlumno = df.loc[7, 5].split(":")[-1].strip()
        matricula = df.loc[6, 5].split(":")[-1].strip()
        tutor = df.loc[4, 5].split(":")[-1].strip()
        periodo = df.loc[3, 5].split(":")[-1].strip()
        gradoGrupo = df.loc[2, 5].split(":")[-1].strip()
        carreraAdscrita = df.loc[1, 5].split(":")[-1].strip()

        # Obtener clases
        hora1 = df.loc[11, 1]
        hora2 = df.loc[12, 1]
        hora3 = df.loc[13, 1]
        hora4 = df.loc[14, 1]
        hora5 = df.loc[15, 1]
        hora6 = df.loc[16, 1]
        hora7 = df.loc[18, 1]

        correoProfesor = df.loc[21, 1]
        
        def materias_por_dia(dia):
            rango = list(range(11, 17)) + list(range(18, 19))
            materias = []
            for i in rango:
                clase = df.loc[i, dia]
                if pd.isna(clase):
                    materias.append("No hay clase")
                else:
                    nombreMateria = " ".join(clase.split())
                    materias.append(nombreMateria.strip())
            return materias

        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        horas = [hora1, hora2, hora3, hora4, hora5, hora6, hora7]
        rango = list(range(2,4)) + list(range(7, 10))
        materias_dias = [materias_por_dia(i) for i in rango]
        materiasVariable = self.obtener_nombre_materia()

        patronesRegex = [re.compile(re.escape(materia)) for materia in materiasVariable]

        def split_text(text, long):
            return '-\n'.join(text[i:i+long] for i in range(0, len(text), long))

        horario_list = []

        print(f"Horario del alumno: {nombreAlumno}")
        for i, hora in enumerate(horas):
            fila = [hora]
            for j, dia, in enumerate(dias_semana):
                materia = materias_dias[j][i]
                coincidencias = [patron.search(materia) for patron in patronesRegex if patron.search(materia)]
                if coincidencias:
                    caracteres_coincidentes = [split_text(coincidencia.group(), 20) for coincidencia in coincidencias]
                    fila.append(" - ".join(caracteres_coincidentes))
                else:
                    fila.append("No hay clase")
            horario_list.append(fila)
        print(f"Carrera: {carreraAdscrita}")
        print(f"Grado y grupo: {gradoGrupo}")
        print(f"Periodo: {periodo}")
        print(f"Tutor: {tutor}")

        # Center content
        col_align = ["center" for i in range(6)]
        print(tabulate.tabulate(horario_list, headers=["H", "L", "M", "X", "J", "V"], tablefmt="fancy_grid", colalign=col_align))
