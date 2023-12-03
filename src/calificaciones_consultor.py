import time
import tabulate
import shutil
from selenium.webdriver.common.by import By

class CalificacionesConsultor:
    def __init__(self, driver):
        self.driver = driver

    def consultando_calificaciones(self, materia):
        terminal_width = shutil.get_terminal_size().columns
        mensaje = f"Consultando calificaciones de {materia}"
        spaces_to_clear = " " * (terminal_width - len(mensaje))
        print(mensaje + spaces_to_clear, end="\r")
        time.sleep(0.1)

    def consultar_calificacion(self):
        self.driver.get("https://agora.utj.edu.mx/consultaCalificacion/index")

        combo_materias_button = self.driver.find_element(By.ID, "comboMaterias")
        options = combo_materias_button.find_elements(By.TAG_NAME, "option")
        div_asistencia = self.driver.find_element(By.ID, "divAsistencia")
        porcentaje_element = div_asistencia.find_element(By.TAG_NAME, "span")

        # Variable para almacenar la salida
        table_data = []

        for option in options:
            materia = option.text
            value = option.get_attribute("value")

            if materia == "Selecciona...":
                continue

            option.click()
            self.consultando_calificaciones(materia)
            time.sleep(1)
            porcentaje = porcentaje_element.text

            if "/" in value:
                calificacion = value.split("/")[1]
                table_data.append([materia, calificacion, f"{porcentaje}%"])
            else:
                table_data.append([materia, "Sin calificación capturada", f"{porcentaje}%"])


        # Mostrar toda la salida al final
        table_headers = ["Materia", "Calificación", "Porcentaje"]
        salida = tabulate.tabulate(table_data, headers=table_headers, tablefmt="grid")
        print(salida)