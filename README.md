# Showcasing Smart Enums

## Introduction

This repo is a sandbox for testing coding techniques to be used in a larger Django application.

One of the main features of this repo is the use of Smart Enums, which are a way to define a set of choices for a model field in Django, while also providing additional functionality to the choices themselves.

We are also testing and showcasing other techniques, such as using childern models to extend the functionality of a parent model, and using abstract models to define common fields and methods that can be shared among multiple models. Note that the extra properties of the childeren models are stores in a separate table, whereas the common properties are stored in the parent table. But all properties can be accessed from the child instance, as if they were all stored in the same table.

## Installation

This assumes that you have Python 3.6 or higher installed on your machine, as well as pip.

### Windows installation

- create a root project folder and navigate into it
- `clone the repository inside the project folder
- `python -m venv env` : to create a virtual environment
- `env\Scripts\activate` : to activate it using a build in script
- `pip install -r requirements.txt -r requirements-dev.txt` : to install all the dependencies
- `cp .env.example .env` : to create a .env file, using the example file as a template (note: the .env file should not be committed to the repository, as it may contain sensitive information)
- adjust the .env file to your needs
- `python manage.py migrate` : to create the database schema
- `python manage.py runserver` : to start the server

## Testing

### General instructions for testings

To run the tests, either set the `DJANGO_TESTING=True` variable in the `.env` file and run the following command in the terminal: `python manage.py test`

Or run the following command in the terminal: `set DJANGO_TESTING=True && python manage.py test` (in Windows) or `export DJANGO_TESTING=True && python manage.py test` (in Linux)

To run a specific test file only, run the following command in the terminal: `python manage.py test <path_to_test_file>` (in Windows)

### Specific tests to run

- `python manage.py test order.tests -v 2` : make sure to add the `-v 2` flag to see the output of the print statements in the tests. Then check out the database. You will see where the extra properties are stored for the child models.

- `python manage.py test payment_term.tests -v 2` : make sure to add the `-v 2` flag to see the output of the print statements in the tests. You will see that the extra properties of the enums can be accessed directly from the instance's properties which refererence the enums.
