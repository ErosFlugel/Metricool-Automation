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
5. In the Installer folder: run the MetriAutomation_WINDOWS_setup.exe file
