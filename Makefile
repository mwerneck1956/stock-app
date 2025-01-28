CURRENT_DIR := $(shell pwd)
export GOOGLE_APPLICATION_CREDENTIALS=$(CURRENT_DIR)/credentials.json

.PHONY: run
VENV_PATH = ./env

active-environment: create-env load-env install

make create-env:
	@echo "Creating Python virtual environment..."
	@python -m venv $(VENV_PATH)

load-env:
	@echo "Activating Python virtual environment..."
	@source $(VENV_PATH)/Scripts/activate || source $(VENV_PATH)/bin/activate
	
install:
	@echo "Installing dependencies..."
	$(VENV_PATH)/Scripts/pip install -r requirements.txt || source $(VENV_PATH)/bin/pip install -r requirements.txt

run:
	echo $(GOOGLE_APPLICATION_CREDENTIALS)
	@echo "Running script..."
	$(VENV_PATH)/Scripts/python ./src/main.py
