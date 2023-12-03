import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils import Colors

class AgoraSesion:
    def __init__(self, driver):
        self.driver = driver

    def iniciar_sesion(self, usuario, contrasena):
        sys.stdout.write("\033[F")
        self.driver.get("https://agora.utj.edu.mx/Account/Login")

        usuario_input = self.driver.find_element(By.ID, "usuario")
        usuario_input.send_keys(usuario)

        contrasena_input = self.driver.find_element(By.ID, "contrasena")
        contrasena_input.send_keys(contrasena)

        iniciar_sesion_button = self.driver.find_element(By.ID, "BtnIniciar")
        iniciar_sesion_button.click()

        try:
            WebDriverWait(self.driver, 5).until(EC.url_to_be("https://agora.utj.edu.mx/home/index"))
        except TimeoutException:
            # Limpiar la última línea de la consola
            print(Colors.colorize("Error: Usuario o contraseña incorrectos.", Colors.RED))
            sys.exit(1)

