# FlexUp Backend API Server

## Introduction

This is the backend API server for the FlexUp project. It is built using Django and Django REST framework.

## Installation

This assumes that you have Python 3.6 or higher installed on your machine, as well as pip.

### Windows installation

- create a root project folder and navigate into it
- `gh repo clone CyberSinister/FlexUp .` : to clone the repository inside the project folder <!-- Fab→Fahad 202410-01: we should rename/move this repo to https://github.com/fabrizionastri/flexup-django-backend -->
- `python -m venv env` : to create a virtual environment <!-- Fab→Fahad 202410-01: we should rename this to .venv -->
- `env\Scripts\activate` : to activate it using a build in script
- `pip install -r requirements.txt -r requirements-dev.txt` : to install all the dependencies
- `cp .env.example .env` : to create a .env file, using the example file as a template (note: the .env file should not be committed to the repository, as it may contain sensitive information)
- adjust the .env file to your needs
- `python manage.py migrate` : to create the database schema
- `python manage.py runserver` : to start the server

## Testing

To run the tests, either set the `DJANGO_TESTING=True` variable in the `.env` file and run the following command in the terminal: `python manage.py test`

Or run the following command in the terminal: `set DJANGO_TESTING=True && python manage.py test` (in Windows) or `export DJANGO_TESTING=True && python manage.py test` (in Linux)

To run a specific test file only, run the following command in the terminal: `python manage.py test <path_to_test_file>` (in Windows)
