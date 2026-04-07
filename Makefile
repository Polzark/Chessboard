VENV_DIR=env
PYTHON=python3
PIP=$(VENV_DIR)/bin/pip

all: install

system-deps:
	sudo apt-get update
	sudo apt-get install -y i2c-tools libgpiod-dev python3-libgpiod

venv:
	$(PYTHON) -m venv $(VENV_DIR) --system-site-packages

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

setup: system-deps install

clean:
	rm -rf $(VENV_DIR)