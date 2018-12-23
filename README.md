[![Build Status](https://travis-ci.com/llwasampijja/ireporter-challenge-two.svg?branch=develop)](https://travis-ci.com/llwasampijja/ireporter-challenge-two)   [![Coverage Status](https://coveralls.io/repos/github/llwasampijja/ireporter-challenge-two/badge.svg?branch=develop)](https://coveralls.io/github/llwasampijja/ireporter-challenge-two?branch=develop)   [![Maintainability](https://api.codeclimate.com/v1/badges/77dbdd739153972a3f77/maintainability)](https://codeclimate.com/github/llwasampijja/ireporter-challenge-two/maintainability)

# iReporter
Corruption is a huge bane to Africa’s development. African countries must develop novel and  localised solutions that will curb this menace, hence the birth of iReporter. iReporter enables  any/every citizen to bring any form of corruption to the notice of appropriate authorities and the  general public. Users can also report on things that needs government intervention.


# iReporter API Endpoints
This project is about a set of endpoints for the ireporter App. The data used is stored in memory using data structures and not a database.
## The Features Include:
* Create a red-flag.
* Get a red-flag by id.
* Get all red-flags.
* Update a red-flag by id
* Delete a red-flag by id.

## Table of Contents
- [Language and Tools used](##Language)
- [Installing](##Installing)
- [Running the application](##RunningtheApplication)
- [Unit Testing the app](##UnitTestingtheApplication)
- [Available Version](##URLVersioning)
- [Deployed Version](##DeployedVersion)
- [Documentation](##Documentation)

## Language and Tools Used
### Tools used include:
* [Python 3.7](https://www.python.org)
* Pip - A python package installer
* Virtualenv
* Git
* VSCode (IDE)

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
    `cd ireporter-challenge-two`
- Step 4: Switch to the "develop" branch using the command below.
`git checkout feature`

##### Set Up the Virtual Environment
Inorder to set up the virtual environment, you need to install the python package called virtualenv using pip. Run the command below to install it.
`pip install virtualenv` to install virtualenv
`virtualenv env`  to create a virtual environment named env
`env/scripts/activate.bat` to activate your virtual environment.
`env/scripts/deactivate.bat` to deactivate your virtual environment at anytime you feel like.

### Installing Requirements
After setting up and activating your virtual environment, you need to install all the packages required by the project. All these requirements are listed and stored in the requirements.txt file in the root folder of the project.
While in this folder, run the command below to install these requirements.
`pip install -r requirements.txt`

And now you have successfully cloned the project and also configured it to run on your computer.


## Running the Application
To run this application, while in the root folder of the project via the Terminal or command prompt, run the command below:

`py main.py`

On running that command, the application server will be launched and the URL to that server will be shown to you in the command-line/terminal.

#### Trying out the different Endpoints using postman
|Endpoint|Endpoint Purpose|Allowed HTTP Method|Requirements|
|---|---|---|---|
| /red-flags  | Get red-flags  |GET  | None |
| /red-flags/redflag_id | Get red-flag of the specified id  |GET  |None  |
| /red-flags | Create a red-flag  |POST  |•	created_by (String), location (String), status (String), images ([String, String]), videos ([String, String]), comment (String) |
| /red-flags/redflag_id/location  | Edit location of a red-flag of specicif id  |PATCH  |•	location(String) |
| /red-flags/redflag_id  | Delete a red-flag of specific id  |DELETE  |None  |


## Unit Testing the Application
* In order to run unit tests for this application, you must install pytest, pytest-cov and coverage installed on your pc or virtual environment.
* While in the root of the project, run the command below to run the unit tests and also generate a coverage report.
    `pytest --cov`

## URL Versioning
The endpoints of this application have been versioned. The current version is one (1); i.e.: `api/v1`

## Deployed Version
### Heroku
This API is deployed on heroku. Find it [here](https://ireporter-challenge-two.herokuapp.com/api/v1/red-flags "iReporter on Heroku")
## API Documentation
The API Endpoints of this project have been documented using postman. The doumentation can be found [here](https://documenter.getpostman.com/view/5689256/Rzn8QMm9 "IReporter Documentation")
