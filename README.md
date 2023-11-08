# Recipe API

[Project Description]

## Table of Contents

- [Features](#features)
- [Installation - Requirements](#installation)
- [Endpoints](#endpoints)

## Features

- still under construction

## Installation - Requirements

* docker >= 24.0.6
  ```docker --version```
* docker-compose >= v2.23.0
  ```docker-compose --version```
* python >= 3.10
  ```This is the case when you start the project without docker-compose```
* PostgreSQL >= 16
  ```this is the case when you start the project without docker-compose```

### Development Environment Set Up

#### Start project directly on your host

#### Virtual Environment Set up

```bash
  python -m venv <path_to_env>
  source <path_to_env>/bin/activate
  
  #Case When Your OS Is Windows
  venv\Scripts\activate  #Optional When It Does Not Work Search For <activate.bat> File
```

#### Initialize database

```bash
  python manage.py makemigrations
  python manage.py migrate
```

#### Start API on localhost

```bash
python manage.py runserver
```

### Start project using docker-compose [This is preferred way]

#### Build and start containers

This will fetch/build images and start containers. Migration command will be run during startup.

```bash
  docker-compose up --build
```

#### Working with running container

* When container is running

```bash
docker-compose exec web_api <your_command>
```

* Without running container

```bash
docker-compose run --rm web_api <your_command>
```

You can run any command you would run on you host machine...
<your_command> examples:

* python manage.py makemigrations
* python manage.py migrate
* python manage.py startapp <app_name>
* python manage.py createsuperuser

## Endpoints

### Auth

- **Register**

  `POST /user/register/`

  Endpoint to register a new user.

  Request body:
  ```json
  {
    "email": "user@example.com",
    "first_name": "example_first_name",
    "last_name": "example_last_name",
    "password": "example_password",
    "confirm_password": "example_confirm_password"
  }
  ```
- **Log In**

  `POST /user/login/`

  Endpoint to log in with existing user.

  Request body:
  ```json
  {
    "email": "user@example.com",
    "password": "example_password"
  }
  ```
  Endpoint returns Refresh and Access Token  
  **Note:** Use access token to login in the system
- Response body:
  ```json
  {
    "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU",
    "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"
  }
  ```

### Profile

- **Profile**

  `GET /user/profile/`

  Endpoint for user to view their profile.

  Response body:
  ```json
  {
    "email": "user@example.com",
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "competence_level": 0,
    "date_joined": "DateTime"
  }
  ```
    `PATCH /user/profile/`

  Endpoint for user to update their profile.

  Request body:
  ```json
  {
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "competence_level": 0
  }
  ```
- **Password Change**

  `GET /user/change/password/`

  Endpoint for user to change their password.

  Request body:
  ```json
  {
    "old_password": "string",
    "new_password": "string",
    "confirm_password": "string"
  }
  ```