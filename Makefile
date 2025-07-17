NAME=farmaEnv

all: run

run: req
	@echo "Running the application..."
	clear
	$(NAME)/bin/python3.10 main.py

req: $(NAME)
	@echo "Installing requirements..."
	$(NAME)/bin/pip install -r requirements.txt

$(NAME):
	@echo "Creating virtual environment..."
	python -m venv $(NAME)