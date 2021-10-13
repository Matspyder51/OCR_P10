# Openclassrooms Project 10

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

## To start

### Requirements

- Python 3

### Installation

- Clone or download this repository, extract it inside a folder if necessary, then open a command prompt inside this folder.

- In the command prompt, create a new environment for the python project :

##### (You need the venv package from PiP to do it, if you don't have it, please write `pip install venv` to install it)

To create a new environment, write this command :

`virtualenv env`

Then you need to activate it :

### Windows :

```bash
cd env/Scripts

activate

cd ../..
```

### Linux/Mac Os:

```bash
source env/Scripts/activate
```

And finally, you can install the required packages for the project :

`pip install -r requirements.txt`

## Usage

Inside the project folder run the following commands :

`py manage.py runserver`

2 defaults users are available :
 - Username: admin / Password: admin
 - Username: test / Password: test


## Built with

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django Rest](https://www.django-rest-framework.org/)