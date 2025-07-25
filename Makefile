
VENV_NAME=myLittleFarmaEnv

all: install
	npm start

install: venv
	npm run load

venv:
	python3 -m venv $(VENV_NAME)

