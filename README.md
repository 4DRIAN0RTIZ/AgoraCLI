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
   1. [Desarrollo de nuevas funcionalidades](#desarrollo-de-nuevas-funcionalidades)
6. [Licencia](#licencia)

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

## Windows

Importante ejecutarlo desde PowerShell como administrador.

```powershell
Invoke-WebRequest -Uri https://raw.githubusercontent.com/4DRIAN0RTIZ/AgoraCLI/master/install.ps1 -OutFile install.ps1
.\install.ps1
```

Pueden estar seguros de que el instalador es seguro, aunque les recomiendo **SIEMPRE** ver que van a instalar antes de ejecutar cualquier cosa.

## Uso

```bash
agoracli -m <matricula> -c | -a | -ho
```

### Ejemplo

```bash
agoracli -m 12345678 -c # Muestra las calificaciones
agoarcli -m 12345678 -a # Muestra el adeudo y las referencias de pago.
agoracli -m 12345678 -ho # Muestra el horario
```

## Contribuciones

Si encuentras algún error o tienes alguna sugerencia, por favor crea un issue o envía un pull request. Y si eres de la Universidad Tecnológica de Jalisco, espero que te sea de utilidad.

### Desarrollo de nuevas funcionalidades

El proyecto está abierto a nuevas funcionalidades, hasta donde nos lo permita la plataforma de Ágora. A continuación listaré algunas de las funcionalidades que me gustaría agregar en un futuro, siéntete libre de implementarlas y hacer un `PR`.

- [X]Consultar los números de referencia para los pagos. [e055712f](https://github.com/4DRIAN0RTIZ/AgoraCLI/commit/e05712fd3dea9bb2b5b8902f45f793fa64731875)
- [ ] Enviar solicitud de atención psicológica.
- [ ] Cambiar contraseña.
- [ ] Consultar y actualizar datos personales.
- [ ] Consultar el reporte de estadía.

La documentación siempre es importante, y puede mejorar. Si encuentras algún error ortográfico, o crees que algo puede mejorarse, no dudes en crear un issue o enviar un pull request. Todos, absolutamente todos los comentarios son bienvenidos y tomados en cuenta.

## Licencia

Este proyecto está licenciado bajo la licencia GPL-3.0. Puedes ver más detalles en el archivo `LICENSE.txt` del repositorio.

Es importante mencionar que el proyecto de ÁgoraCLI de momento no está afiliado de ninguna manera con la Universidad Tecnológica de Jalisco, ni con la plataforma de Ágora, por lo que no es OFICIAL.

AgoraCLI es un proyecto de código abierto, y siempre lo será. Siéntete libre de usarlo, modificarlo y distribuirlo, siempre y cuando respetes la licencia.

AgoraCLI Copyleft 🄯 2024. Originalmente creado por Oscar Adrian Ortiz Bustos.
