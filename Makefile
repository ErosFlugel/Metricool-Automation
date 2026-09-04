# Path to inno directory
INNO_COMPILER := "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

.PHONY: dev build test clean update

# Update automation 
update:
# delete the installer folder
	@if exist installer rmdir /s /q installer

    # (pyinstaller)
	pyinstaller MetricoolAutomation.spec

	@echo Compiling Inno Setup installer...
	$(INNO_COMPILER) "Inno_setup_MetriAutomation.iss"

	@echo Launching the generated file...
	@cmd /c start "" "installer\MetriAutomation_WINDOWS_setup.exe"

# Run the project (dev)
run:
    # (Python)
	python main.py

# Install project dependencies
install:
    # (Python)
	pip install -r requirements.txt

# Unit Testing
test:
    # (Python)
	pytest

# Cleaning temporary files or cache
clean:
    # (Python)
	find . -type d -name "__pycache__" -exec rm -rf {} +