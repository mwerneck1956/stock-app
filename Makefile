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

prefect-login:
	@echo "Logging into Prefect Cloud..."
	@if [ "$(API_KEY)" = "" ]; then \
		echo "Error: API_KEY parameter is missing. Use 'make prefect-login API_KEY=<your_api_key>'."; \
		exit 1; \
	fi
	@if [ -d "$(VENV_PATH)/bin" ]; then \
		$(VENV_PATH)/bin/prefect cloud login --key $(API_KEY); \
	else \
		$(VENV_PATH)/Scripts/prefect cloud login --key $(API_KEY); \
	fi

run:
	@echo $(GOOGLE_APPLICATION_CREDENTIALS)
	@echo "Running script..."
	@if [ -d "$(VENV_PATH)/bin" ]; then \
		$(VENV_PATH)/bin/python ./src/main.py; \
	else \
		$(VENV_PATH)/Scripts/python ./src/main.py; \
	fi

run-storage:
	@echo $(GOOGLE_APPLICATION_CREDENTIALS)
	@echo "Running script..."
	@if [ -d "$(VENV_PATH)/bin" ]; then \
		$(VENV_PATH)/bin/python ./src/storage.py; \
	else \
		$(VENV_PATH)/Scripts/python ./src/storage.py; \
	fi
