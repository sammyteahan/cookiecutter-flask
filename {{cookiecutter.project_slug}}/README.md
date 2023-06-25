# {{ cookiecutter.project_name }}

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

#### 🚧 System Requirements

Here are a few things you'll need globally available on your machine.

- [Nodejs 18.x](https://nodejs.org/en)
- [Docker](https://www.docker.com/)
- [Python 3.8](https://www.python.org/)
- [asdf](https://asdf-vm.com/) (optional)

#### 🏎 Setup

**Environment**
Copy over the environment variables:

```bash
cp .env.example .env
```

**Docker**
Spin up the docker containers. The first time you run this it'll take a minute or two and you'll need to pass the `--build` flag. Once everything is setup the build flag can be omitted in normal day-to-day development.

```bash
docker comopse up --build
```

**Database**
Initialize the database prior to using the app. This app uses [Flask-DB](https://github.com/nickjj/flask-db) to manage database state and migrations. In development `Flask-DB` makes life easy by automatically picking up model changes and representing them in the database. In production, you'll want to use traditional migration patterns. Anyways, to make sure the development databases are setup correctly run:

```bash
./run flask db reset --with-testdb
```

This will create two databases. One for development and one for running tests. The command will also run any seeds you have set up. You can run this command anytime you want to reset the database to a fresh state in development.


**Other**
The previous command leverages a custom `./run` script. In general this just makes running commands in Docker easier. It's just a bash script so you can see the file itself for more example. Some common commands include:

```bash
./run shell # connect to the running web container
./run test # run pytest
./run lint # run flake8 linting
./run pip3:install # run pip3 install in a web container and save requirement files
```