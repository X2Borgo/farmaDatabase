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
	if [ ! -d "$(NAME)" ]; then \
		conda create --prefix ./$(NAME) python=3.10 pandas; \
	else \
		echo "Virtual environment already exists."; \
	fi

clean:
	@echo "Cleaning up..."
	rm -rf $(NAME)

test: req
	@echo "Running tests..."
	$(NAME)/bin/python3.10 test.py<<<<

val: req
	@echo "checking valgrind memory leaks..."
	valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes $(NAME)/bin/python3.10 main.py