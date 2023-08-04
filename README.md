# Installation

## Cloning project

### SSH
```shell
git clone git@github.com:SaD-Pr0gEr/fastapi_template.git
```

### HTTPS
```shell
git clone https://github.com/SaD-Pr0gEr/fastapi_template.git
```

## Installing dependencies
```shell
poetry install
poetry shell
```

## Setting up environment vars
* rename `app/example.envs` to `.envs`
* remove `example` from every file name in `app/example.envs`(`aka app/.envs`)
* You should get something like this `app/.envs/.env`/`app/.envs/db.env`/`app/.envs/server.env`
* Rename all example values to actual vars

## Running project
```shell
cd app
uvicorn main:app --reload
```
