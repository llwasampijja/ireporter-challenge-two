[![Build Status](https://travis-ci.com/llwasampijja/ireporter-challenge-two.svg?branch=develop)](https://travis-ci.com/llwasampijja/ireporter-challenge-two)   [![Coverage Status](https://coveralls.io/repos/github/llwasampijja/ireporter-challenge-two/badge.svg?branch=develop)](https://coveralls.io/github/llwasampijja/ireporter-challenge-two?branch=develop)   [![Maintainability](https://api.codeclimate.com/v1/badges/77dbdd739153972a3f77/maintainability)](https://codeclimate.com/github/llwasampijja/ireporter-challenge-two/maintainability)

# iReporter
Corruption is a huge bane to Africa’s development. African countries must develop novel and  localised solutions that will curb this menace, hence the birth of iReporter. iReporter enables  any/every citizen to bring any form of corruption to the notice of appropriate authorities and the  general public. Users can also report on things that needs government intervention.


# iReporter API Endpoints
This project is about a set of endpoints for the ireporter App. The data used is stored in memory using data structures and not a database.
## The Features Include:
* Sign-up a user.
* Login a user.
* Create a red-flag incident.
* Get a red-flag incident by id.
* Get all red-flag incidents.
* Update a red-flag incident's location by id.
* Update a red-flag incident's status by id.
* Delete a red-flag incident by id.
* Create an intervention incident.
* Get all intervention incidents.
* Get an intervention incident by id.
* Update an intervention incident's location by id.
* Update an intervention incident's status by id.
* Delete an intervention incident by id.
* Get all users.
* Update a user's role by id.

## Table of Contents
- [Project Description](#ireporter)
- [Language and Tools used](#language-and-tools-used)
- [Installing](#installing)
- [Running the application](#running-the-application)
- [List of Endpoints](#endpoints-included)
- [Unit Testing the app](#unit-testing-the-application)
- [System Security](#system-security)
- [Available Version](#url-versioning)
- [Deployed Version](#deployed-version)
- [Documentation](#api-documentation)

## Language and Tools Used
### Tools used include:
* [Python 3.7](https://www.python.org)
* [Flask](http://flask.pocoo.org/)
* [JWT](https://jwt.io/)
* [Pip - A python package installer](https://pypi.org/project/pip/)
* [Virtualenv](https://pypi.org/project/virtualenv/)
* [Git](https://git-scm.com/downloads)
* [VSCode (IDE)](https://code.visualstudio.com/)
* [Open API](https://www.openapis.org/)
* [Swagger](https://swagger.io/)
* [Postman](https://www.getpostman.com/)

## Installing
### Pre-Installations
##### Python3 Installation on Windows PC
Head to the python's 0fficial [website](https://www.python.org) and download python3.
After downloading it, double click the executable file and follow the prompts to install python on your machine.
##### Git Installation on Windows PC
You also need to install git so as to be able to switch between the different branches of this project. Head to [Git ](https://git-scm.com/downloads "Official Git Download Site")  and the executable file.
Double click the executable file to run the installer and follow the prompts to install it on your windows PC. The process of installing git installs two tools which you can use, that is, the Git Bash and Git GUI. For this project, you are going to use Git Bash for all the command-line prompt /terminal commands.
##### Postman installation On Windows PC
You will need to install postman (or any of its alternatives) so as to test the different endpoints in this application. You won’t be able to test the endpoints in the browser since they use other HTTP methods other than the “GET” method.
Postman is available as a Google Chrome extention (getting outdated) and as a native application. Any one of the options you choose will work just fine.

##### Cloning the Repository to Your Local Machine (Windows PC)
- Step 1: Open the git bash tool and navigate to where you want to place this project.
- Step 2: Now run this command in git bash CLI.

    `git clone https://github.com/llwasampijja/ireporter-challenge-two`

    This will copy the entire project onto your local machine. Project name should be “ireporter-challenge-two”
- Navigate to the root folder of the project in git bash cmd using the command below.
- 
    `cd ireporter-challenge-two`

- Step 4: Switch to the "develop" branch using the command below.

`git checkout feature`

##### Set Up the Virtual Environment
Inorder to set up the virtual environment, you need to install the python package called virtualenv using pip. Run the command below to install it.
- `pip install virtualenv` to install virtualenv
- `virtualenv env`  to create a virtual environment named env
- `env/scripts/activate.bat` to activate your virtual environment.
- `env/scripts/deactivate.bat` to deactivate your virtual environment at anytime you feel like.

### Installing Requirements
After setting up and activating your virtual environment, you need to install all the packages required by the project. All these requirements are listed and stored in the requirements.txt file in the root folder of the project.
While in this folder, run the command below to install these requirements.
- `pip install -r requirements.txt`

And now you have successfully cloned the project and also configured it to run on your computer.


## Running the Application
To run this application, while in the root folder of the project via the Terminal or command prompt, run the command below:
- `py main.py`

On running that command, the application server will be launched and the URL to that server will be shown to you in the command-line/terminal.

#### Endpoints included
|Endpoint|Endpoint Purpose|Allowed HTTP Method|Requirements|
|---|---|---|---|
| [/](https://ireporter-challenge-two.herokuapp.com/api/v1)  | Index Endpointr  |GET  | None  |
| [/auth/register](https://ireporter-challenge-two.herokuapp.com/api/v1/auth/register)  | Register/signup a user  |POST  | firstname (String), lastname (String), othernames (String), email (String), phonenumber (String), username (String), password (String)  |
| [/auth/login](https://ireporter-challenge-two.herokuapp.com/api/v1/auth/login)  | Login/sign-in a user  |POST, GET  | username (String), password (String)  |
| [/red-flags](https://ireporter-challenge-two.herokuapp.com/api/v1/red-flags) | Create a red-flag  |POST  |	location (String), images ([String, String]), videos ([String, String]), title (String), comment (String) |
| [/red-flags](https://ireporter-challenge-two.herokuapp.com/api/v1/red-flags)  | Get red-flags  |GET  | None |
| [/red-flags/redflag_id](https://ireporter-challenge-two.herokuapp.com/api/v1/red-flags/3) | Get red-flag of the specified id  |GET  |None  |
| [/red-flags/redflag_id/location](https://ireporter-challenge-two.herokuapp.com/api/v1/red-flags/3/location)  | Edit location of a red-flag of specicif id  |PATCH  |	location(String) |
| [/red-flags/redflag_id/status](https://ireporter-challenge-two.herokuapp.com/api/v1/red-flags/3/status)  | Edit status of a red-flag of specific id  |PATCH  | status (String)  |
| [/red-flags/redflag_id](https://ireporter-challenge-two.herokuapp.com/api/v1/red-flags/3)  | Delete a red-flag of specific id  |DELETE  |None  |
| [/interventions](https://ireporter-challenge-two.herokuapp.com/api/v1/interventions) | Create a intervention  |POST  |	location (String), images ([String, String]), videos ([String, String]), title (String), comment (String) |
| [/interventions](https://ireporter-challenge-two.herokuapp.com/api/v1/interventions)  | Get interventions  |GET  | None |
| [/interventions/intervention_id](https://ireporter-challenge-two.herokuapp.com/api/v1/interventions/5) | Get intervention of the specified id  |GET  |None  |
| [/interventions/intervention_id/location](https://ireporter-challenge-two.herokuapp.com/api/v1/interventions/5/location)  | Edit location of a intervention of specicif id  |PATCH  |•	location(String) |
| [/interventions/intervention_id/status](https://ireporter-challenge-two.herokuapp.com/api/v1/interventions/5/status)  | Edit status of a intervention of specific id  |PATCH  |• status (String)  |
| [/interventions/intervention_id](https://ireporter-challenge-two.herokuapp.com/api/v1/interventions/5)  | Delete a intervention of specific id  |DELETE  |None  |
| [/users](https://ireporter-challenge-two.herokuapp.com/api/v1/users)  | Ge all users  |GET  | None  |
| [/users/user_id](https://ireporter-challenge-two.herokuapp.com/api/v1/users/10)  | Edit user's role  |PATCH  | is_admin (Boolean)  |


## Unit Testing the Application
* In order to run unit tests for this application, you must install pytest, pytest-cov and coverage installed on your pc or virtual environment.
* While in the root of the project, run the command below to run the unit tests and also generate a coverage report.
- `pytest --cov`

## System Security
The endpoints of this web application have been secured using JWT (Json Web Tokens).

## URL Versioning
The endpoints of this application have been versioned. The current version is one (1); i.e.: `api/v1`

## Deployed Version
### Heroku
This API is deployed on heroku. Find it [here](https://ireporter-challenge-two.herokuapp.com/api/v1/red-flags "iReporter on Heroku")
## API Documentation
The API Endpoints of this project have been documented using Swagger UI and postman.
* The Swagger-UI documentation can be found [here](https://ireporter-challenge-two.herokuapp.com/api/v1/docs "iReporter Swagger-UI Documentation")
* The Postman documentation can be found [here](https://documenter.getpostman.com/view/5689256/Rzn8QMm9 "IReporter Documentation")