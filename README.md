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
* Rename `app/example.envs` to `.envs`
* Remove `example` from every file name in `app/example.envs`(`aka app/.envs`)
* They should look like this `app/.envs/.env`/`app/.envs/db.env`
* Rename all example values to actual values

## Setting up config
* Rename `app/example.config.toml` to `app/config.toml`
* Rename all example values to actual values

## Running project
```shell
cd app
uvicorn main:app --reload
```
