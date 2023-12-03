# AgoraCLI

## Descripción

AgoraCLI es una herramienta de línea de comandos para consultar las calificaciones de los estudiantes de la Universidad Tecnológica de Jalisco.

## Instalación
Descargar el Driver de Chrome
```bash
wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/linux64/chrome-linux64.zip
# Descomprimir el archivo
7z x chrome-linux64.zip
# Mover el archivo a /usr/bin
mv chrome-linux64 /usr/bin
```

Descargar el repositorio

```bash
pip install -r requirements.txt
```
## Uso

```bash
python main.py -u <matricula>
```

### Ejemplo
```bash
python main.py -u 123456
```
## Contribuciones

Si encuentras algún error o tienes alguna sugerencia, por favor crea un issue o envía un pull request. Y si eres de la Universidad Tecnológica de Jalisco, espero que te sea de utilidad.
