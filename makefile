PYTHON_VERSION = 3.12.6
VENV = .venv
UV_INSTALLER = uv-installer-latest.exe

ifeq ($(OS),Windows_NT)
    PYTHON = python
    PIP = $(VENV)\Scripts\pip
    PYTHON_VENV = $(VENV)\Scripts\python
    UV = uv.exe
    NULL_OUTPUT = >nul 2>&1
    UV_DOWNLOAD_URL = https://uv.wtf/releases/latest/windows/$(UV_INSTALLER)
    EXPORT_ENV = set UV_LINK_MODE=copy&&
else
    PYTHON = python3
    PIP = $(VENV)/bin/pip
    PYTHON_VENV = $(VENV)/bin/python
    UV = uv
    NULL_OUTPUT = >/dev/null 2>&1
    UV_DOWNLOAD_URL = https://uv.wtf/releases/latest/linux/uv
    EXPORT_ENV = UV_LINK_MODE=copy
endif

.PHONY: setup run clean check-uv install-uv create-venv

check-uv:
	@echo Checking UV installation...
ifeq ($(OS),Windows_NT)
	@where $(UV) $(NULL_OUTPUT) || (echo UV not found. Installing... && $(MAKE) install-uv)
else
	@which $(UV) $(NULL_OUTPUT) || (echo UV not found. Installing... && $(MAKE) install-uv)
endif

install-uv:
	@echo Downloading UV installer...
ifeq ($(OS),Windows_NT)
	@curl -Lo $(UV_INSTALLER) $(UV_DOWNLOAD_URL)
	@echo Installing UV...
	@$(UV_INSTALLER) /quiet
	@del $(UV_INSTALLER)
else
	@curl -Lo $(UV) $(UV_DOWNLOAD_URL)
	@chmod +x $(UV)
	@mv $(UV) /usr/local/bin/
endif
	@echo UV successfully installed!

create-venv: check-uv
	@echo Checking if virtual environment exists...
ifeq ($(OS),Windows_NT)
	@if exist $(VENV) ( \
		echo Virtual environment already exists. Recreating... && \
		rmdir /s /q $(VENV) \
	)
else
	@if [ -d $(VENV) ]; then \
		echo Virtual environment already exists. Recreating... && \
		rm -rf $(VENV); \
	fi
endif
	@echo Creating new virtual environment with UV...
	@$(UV) venv $(VENV) --python $(PYTHON_VERSION) --link-mode=copy
	@echo Virtual environment successfully created!

install-deps: create-venv
	@echo Checking for requirements.txt...
ifeq ($(OS),Windows_NT)
	@if exist requirements.txt ( \
		echo Installing dependencies from requirements.txt... && \
		$(UV) pip install -r requirements.txt --link-mode=copy \
	) else ( \
		echo No requirements.txt found. Using UV sync... && \
		$(UV) sync --link-mode=copy \
	)
else
	@if [ -f requirements.txt ]; then \
		echo Installing dependencies from requirements.txt... && \
		$(EXPORT_ENV) $(UV) pip install -r requirements.txt; \
	else \
		echo No requirements.txt found. Using UV sync... && \
		$(EXPORT_ENV) $(UV) sync --link-mode=copy; \
	fi
endif
	@echo Dependencies installed successfully!

setup: install-deps
	@echo Setup completed!

run: setup
	@$(PYTHON_VENV) main.py

clean:
ifeq ($(OS),Windows_NT)
	@if exist $(VENV) rmdir /s /q $(VENV)
else
	@rm -rf $(VENV)
endif