# Metricool-Automation

An automation that fills a google sheet with information from metricool api

Create venv -> python -m venv .venv
Activate venv -> `source .venv/Scripts/activate`
instal dependencies -> `pip install -r requirements.txt`
Make sure you have selected the venv in visual studio code, ctrl + shift + P, create environment, venv, use existing

Set Up requirements.txt -> `pip freeze > requirements.txt`

create the .exe file after some changes

1. uninstall the actual program from program C:\Program Files\Metri-Automation
2. Delete the installer folder in the git project
3. on the active virtual environment and in the root folder of the project run in the terminal: `pyinstaller MetricoolAutomation.spec`
4. open the Inno_setup_MetriAutomation.iss, Save, Build -> Compile (Ctrl + F9)
5. In the Installer folder: run the MetriAutomation_WINDOWS_setup.exe file (you can share this one with others)

## Guía de Instalación para "Metricool Automation"

### Paso 1: Desbloquear el archivo manualmente

Windows suele marcar los archivos descargados como "no seguros" de forma automática.

1. Haz clic derecho sobre el archivo MetriAutomation_WINDOWS_setup.exe.

2. Selecciona Propiedades.

3. En la pestaña General, busca abajo del todo una sección llamada Seguridad.

4. Verás un texto que dice: "Este archivo proviene de otro equipo y podría bloquearse para ayudar a proteger este equipo", Marca la casilla que dice Desbloquear y dale a Aceptar.

### Paso 2: Agregar una Exclusión en Seguridad de Windows

Si el error persiste, es probable que el antivirus (Windows Defender) esté impidiendo la ejecución del instalador del proyecto Metricool-Automation.

1. Abre el menú de Inicio y busca "Seguridad de Windows".

2. Ve a Protección contra virus y amenazas.

3. Busca "Administrar la configuración" (debajo de Configuración de protección contra virus y amenazas).

4. Baja hasta encontrar Exclusiones y haz clic en "Agregar o quitar exclusiones".

5. Haz clic en Agregar una exclusión -> Archivo y selecciona el instalador.

Nota: Una vez instalado, también podrías agregar la carpeta donde se instaló el programa (en Archivos de programa) para que el .exe principal no sea bloqueado después.

### Paso 3: Verificar el "Modo S" (Solo para Windows Home)

Muchos equipos nuevos con Windows 11 Home vienen con el "Modo S" activado, que solo permite instalar aplicaciones de la Microsoft Store.

1. Ve a Configuración -> Sistema -> Activación.

2. Busca una sección que diga "Modo S".

3. Si está activado, aparecerá una opción para "Salir del Modo S". (Ojo: esto es un cambio permanente, pero es necesario para ejecutar cualquier programa .exe externo).
