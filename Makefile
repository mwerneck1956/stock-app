CURRENT_DIR := $(shell pwd)
export GOOGLE_APPLICATION_CREDENTIALS=$(CURRENT_DIR)/credentials.json

.PHONY: run
VENV_PATH = ./env

active-environment: create-env load-env install

create-env:
	@echo "Creating Python virtual environment..."
	@python -m venv $(VENV_PATH)

load-env:
	@echo "Activating Python virtual environment..."
	@if [ -d "$(VENV_PATH)/bin" ]; then \
		. $(VENV_PATH)/bin/activate; \
	else \
		. $(VENV_PATH)/Scripts/activate; \
	fi

install:
	@echo "Installing dependencies..."
	@if [ -d "$(VENV_PATH)/bin" ]; then \
		$(VENV_PATH)/bin/pip install -r requirements.txt; \
	else \
		$(VENV_PATH)/Scripts/pip install -r requirements.txt; \
	fi

run:
	@echo $(GOOGLE_APPLICATION_CREDENTIALS)
	@echo "Running script..."
	@if [ -d "$(VENV_PATH)/bin" ]; then \
		$(VENV_PATH)/bin/python ./src/main.py; \
	else \
		$(VENV_PATH)/Scripts/python ./src/main.py; \
	fi
