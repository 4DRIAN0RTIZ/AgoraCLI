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
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import Clear

class HorarioConsultor:
    def __init__(self, driver, download_path):
        self.driver = driver
        self.download_path = download_path


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
        # Elimina archivos anteriores
        files = os.listdir(self.download_path)
        for file in files:
            if file.startswith("Horario") and file.endswith(".xlsx"):
                os.remove(os.path.join(self.download_path, file))

        # Esperar hasta que un nuevo archivo se descargue
        while True:
            files = os.listdir(self.download_path)
            horario_files = [f for f in files if f.startswith("Horario") and f.endswith(".xlsx")]
            if horario_files:
                time.sleep(1)  # Asegurar que la descarga esté completamente finalizada
                break

    def open_file(self):
        files = os.listdir(self.download_path)
        horario_files = [f for f in files if f.startswith("Horario") and f.endswith(".xlsx")]

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


        
        def obtener_horas(df, inicio=11, fin=20, columna=1):
            horas = []
            horas_necesarias = 7
            i = inicio
            indices_validos = []
            max_fila = df.shape[0]  # Obtiene el número máximo de filas
            
            try:
                while len(horas) < horas_necesarias and i < max_fila:
                    hora = df.loc[i, columna]
                    # Verifica formato de hora (HH:MM-HH:MM)
                    if isinstance(hora, str) and len(hora.split("-")) == 2:
                        horas.append(hora)
                        indices_validos.append(i)
                    i += 1
                
                # Si no se encontraron suficientes horas
                if len(horas) < horas_necesarias:
                    print(f"Advertencia: Solo se encontraron {len(horas)} horas válidas de {horas_necesarias}")
                    # Rellenar con "No disponible" hasta tener 7 horas
                    horas.extend(["No disponible"] * (horas_necesarias - len(horas)))
                    
            except KeyError as e:
                print(f"Error: Índice fuera de rango - {e}")
                horas.extend(["No disponible"] * (horas_necesarias - len(horas)))
            except Exception as e:
                print(f"Error inesperado: {e}")
                horas.extend(["No disponible"] * (horas_necesarias - len(horas)))
            
            return horas, indices_validos

        def materias_por_dia(df, dia, indices):
            """
            Obtiene las materias para un día específico usando los índices válidos
            """
            materias = []
            for i in indices:
                clase = df.loc[i, dia]
                if pd.isna(clase):
                    materias.append("No hay clase")
                else:
                    nombreMateria = " ".join(clase.split())
                    materias.append(nombreMateria.strip())
            
            # Si no hay suficientes materias, rellenar con "No hay clase"
            while len(materias) < 7:
                materias.append("No hay clase")
                
            return materias


        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        horas, indices_validos = obtener_horas(df, inicio=11, fin=21, columna=1)
        rango = list(range(2,4)) + list(range(7, 10))
        materias_dias = [materias_por_dia(df, dia, indices_validos) for dia in rango]
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

        correoProfesor = df.loc[21:30, 1]
        materias_validas = materiasVariable

        for texto in correoProfesor:
            if not isinstance(texto, str) or len(texto.strip()) == 0:
                continue
                
            palabras = texto.split()
            correo = ''
            nombre = []
            materia = []
            
            # Encontrar el correo primero
            for palabra in palabras:
                if '@' in palabra:
                    correo = palabra
                    break
            
            # Separar materia y nombre
            encontro_mayusculas = False
            for palabra in palabras:
                if palabra == correo:
                    break
                if all(c.isupper() for c in palabra if c.isalpha()):
                    encontro_mayusculas = True
                    nombre.append(palabra)
                elif not encontro_mayusculas:
                    materia.append(palabra)
                    
            # Buscar la materia en la lista de materias válidas
            materia_str = ' '.join(materia)
            for materia_valida in materias_validas:
                if materia_str.lower() in materia_valida.lower():
                    materia_str = materia_valida
                    break
                    
            nombre_str = ' '.join(nombre)
            print(f"{materia_str} - {nombre_str} - {correo}")
