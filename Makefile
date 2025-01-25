CURRENT_DIR := $(shell pwd)
export GOOGLE_APPLICATION_CREDENTIALS=$(CURRENT_DIR)/credentials.json

.PHONY: run
VENV_PATH = ./env


load-env:
	@echo "Activating Python virtual environment..."
	@source $(VENV_PATH)/Scripts/activate || source $(VENV_PATH)/bin/activate
	
install:
	@echo "Installing dependencies..."
	$(VENV_PATH)/Scripts/pip install -r requirements.txt

run:
	echo $(GOOGLE_APPLICATION_CREDENTIALS)
	@echo "Running script..."
	$(VENV_PATH)/Scripts/python ./src/main.py
