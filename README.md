# Recipe API

[Project Description]

The Recipe API is a web service designed to manage and interact with a collection of recipes.
This API allows users to perform various actions, such as registering and logging in, managing user
profiles, and handling recipes. Whether you are looking to explore a variety of recipes, create your
own, or update existing ones, this API provides the necessary endpoints to facilitate these operations.

## Table of Contents

- [Features](#features)
- [Installation - Requirements](#installation)
- [Endpoints](#endpoints)

## Features

- **User Authentication**: Register and log in with the API to manage your recipes.
- **User Profiles**: View and update user profiles, including details such as username, first name, last name, and
  competence level.
- **Password Change**: Change your password securely using the provided endpoint.
- **Recipe Management**: Create, retrieve, update, and delete recipes. Explore a list of all available recipes.

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

- [Auth](#auth)
- [Profile](#Profile)
- [Recipes](#Recipes)

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

  `POST /user/change/password/`

  Endpoint for user to change their password.

  Request body:
  ```json
  {
    "old_password": "string",
    "new_password": "string",
    "confirm_password": "string"
  }
  ```

### Recipes

- **Get All Recipes**

  `GET /recipes/all/`

  Endpoint for user to view all recipes that are available.

  Response body:
  ```json
  {
    "title": "string",
    "description": "string",
    "preparation_time_minutes": 214,
    "price": "17.58",
    "difficulty_level": 0,
    "created_at": "2023-11-13T09:53:44.041Z"
  }
  ```
- **Create Recipes**

  `POST /recipes/create/`

  Endpoint for user to create recipes.

  Request body:
  ```json
  {
    "title": "string",
    "description": "string",
    "preparation_time_minutes": 2147483647,
    "price": "",
    "difficulty_level": 0,
    "tags": [
      {
        "id": 0,
        "name": "string"
      }
    ],
    "ingredients": [
      {
        "id": 0,
        "name": "string"
      }
    ]
  }
  ```
- **Recipe Details**

  `GET /recipes/recipe-detail/<int:pk>/`

  Endpoint for user to view specific recipe.

  Parameters:
  ```
    id - int
  ```

  Response body:
  ```json
  {
  "title": "string",
  "description": "string",
  "preparation_time_minutes": 2147483647,
  "price": "1.00",
  "difficulty_level": 0,
  "created_at": "2023-11-13T09:53:44.046Z",
  "id": 0,
  "updated_at": "2023-11-13T09:53:44.046Z",
  "link": "string",
  "user": 0,
  "tags": [
    {
      "id": 0,
      "name": "string"
    }
  ],
  "ingredients": [
    {
      "id": 0,
      "name": "string"
    }
  ]
  }
  ```
  `PATCH /recipes/recipe-detail/<int:pk>/`

  Endpoint for creator to partially update specific recipe.

  Parameters:
  ```
    id - int
  ```

  Request body:
  ```json
  {
  "title": "string",
  "description": "string",
  "preparation_time_minutes": 2147483647,
  "price": "1.00",
  "difficulty_level": 0,
  "created_at": "2023-11-13T09:53:44.046Z",
  "updated_at": "2023-11-13T09:53:44.046Z",
  "link": "string",
  "tags": [
    {
      "id": 0,
      "name": "string"
    }
  ],
  "ingredients": [
    {
      "id": 0,
      "name": "string"
    }
  ]
  }
  ```
  `PUT /recipes/recipe-detail/<int:pk>/`

  Endpoint for creator to fully update specific recipe.

  Parameters:
  ```
    id - int
  ```

  Request body:
  ```json
  {
  "title": "string",
  "description": "string",
  "preparation_time_minutes": 2147483647,
  "price": "1.00",
  "difficulty_level": 0,
  "created_at": "2023-11-13T09:53:44.046Z",
  "updated_at": "2023-11-13T09:53:44.046Z",
  "link": "string",
  "tags": [
    {
      "id": 0,
      "name": "string"
    }
  ],
  "ingredients": [
    {
      "id": 0,
      "name": "string"
    }
  ]
  }
  ```
  `DELETE /recipes/recipe-detail/<int:pk>/`

  Endpoint for creator to delete specific recipe.

  Parameters:
  ```
    id - int
  ```

### Tags

- **Get All Tags**

  `GET /tags/all/`

  Endpoint for user to view all tags that are available.

  Response body:
  ```json
  {
    "name": "string",
    "created_at": "2023-11-13T09:53:44.041Z"
  }
  ```

- **Create Tags**

  `GET /tags/create/`

  Endpoint for user to create tags.

  Request body:
  ```json
  {
    "name": "string",
    "description": "string"
  }
  ```
  