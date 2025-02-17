# Definire il nome dell'applicazione e altre variabili
APP_NAME = paralax
PYTHON = python3

# Definire gli obiettivi (targets)
.PHONY: all build run 

# Obiettivo principale
all: build run

# Obiettivo per build
build:
	@echo "Costruzione dell'applicazione $(APP_NAME)..."
	docker build -t $(APP_NAME) .
	@echo "Build completata."

# Obiettivo per run
run:
	@echo "Esecuzione dell'applicazione $(APP_NAME)..."
	docker run --rm -ti --net host $(APP_NAME) $(PYTHON) search_serial.py

# Obiettivo per run
run-paralax:
	@echo "Esecuzione dell'applicazione $(APP_NAME)..."
	docker run --rm -ti --net host $(APP_NAME) $(PYTHON) search_paralax.py