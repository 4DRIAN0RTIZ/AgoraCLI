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
        time.sleep(1)
        # Limpia la consola con shutil
        terminal_width = shutil.get_terminal_size().columns
        print(" " * terminal_width, end="\r")
        table_data = []
        adeudo_div = self.driver.find_element(By.ID, "Totales")
        adeudo_text = adeudo_div.find_element(By.ID, "men")
        adeudo = adeudo_text.text
        table_data.append([adeudo])
        table_headers = ["Adeudo"]
        salida = tabulate.tabulate(table_data, headers=table_headers, tablefmt="grid")
        Clear.linea_anterior()
        print(salida)
