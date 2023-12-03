# AgoraCLI

## Tabla de contenidos
1. [Descripción](#descripción)
2. [Requisitos](#requisitos)
3. [Instalación](#instalación)
    1. [Linux](#linux)
    2. [Windows](#windows)
4. [Uso](#uso)
    1. [Ejemplo](#ejemplo)
5. [Contribuciones](#contribuciones)

## Descripción

AgoraCLI es una herramienta de línea de comandos para consultar las calificaciones de los estudiantes de la Universidad Tecnológica de Jalisco.

## Requisitos

Para un correcto funcionamiento, es necesario tener instalado `ChromeDriver` en su versión `19.0.6045.105` y `Python 3.8.5` o superior.

```bash
wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/linux64/chrome-linux64.zip
# Descomprimir el archivo
7z x chrome-linux64.zip
# Mover el archivo a /usr/bin
mv chrome-linux64 /usr/bin
```

## :information_source: NOTA

Puedes mover el archivo a cualquier directorio, solo asegúrate de agregarlo al `PATH` de tu sistema. Si usas Linux, puedes agregar la siguiente línea al archivo `~/.bashrc` o `~/.zshrc` dependiendo de tu shell.
```bash
export PATH=$PATH:<path_to_chrome_driver>
```
Aunque recomiendo moverlo a `/usr/bin` o `/usr/local/bin` para evitar problemas.

Si estás en Windows, puedes descargarlo desde [aquí](https://googlechromelabs.github.io/chrome-for-testing/#stable). Y seleccionar la versión `19.0.6045.105` junto con la arquitectura de tu sistema.

## Instalación

### Linux

Me tomé la tarea de automatizar el proceso de instalación, por lo que solo es necesario ejecutar el siguiente comando:
```bash
curl -s https://raw.githubusercontent.com/4DRIAN0RTIZ/AgoraCLI/master/install.sh | bash
```

Pueden estar seguros de que el instalador es seguro, aunque les recomiendo **SIEMPRE** ver que van a instalar antes de ejecutar cualquier cosa.


### Windows

En Windows es todavía más fácil, basta con clonar el repositorio.
```bash
git clone https://github.com/4DRIAN0RTIZ/AgoraCLI.git
```
Crear un _entorno virtual_ con Python
```bash
python3 -m venv <virtual_env_name>
# Activarlo
.\<virtual_env_name>\Scripts\activate
```

Instalar las dependencias del archivo `requirements.txt` con `pip`

```bash
pip install -r requirements.txt
```

## Uso

```bash
agoracli -m <matricula>
```

### Ejemplo
```bash
agoracli -m 12345678
```

## Contribuciones

Si encuentras algún error o tienes alguna sugerencia, por favor crea un issue o envía un pull request. Y si eres de la Universidad Tecnológica de Jalisco, espero que te sea de utilidad.

## Licencia

Este proyecto está licenciado bajo la licencia MIT. Puedes ver el archivo `LICENSE` para más información.

