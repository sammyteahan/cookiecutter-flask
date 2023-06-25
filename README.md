# Flask Cookiecutter

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

This is a [cookiecutter](https://github.com/cookiecutter/cookiecutter) template used to bootstrap a new Phoenix backed project. It aims to provide some best practices out of the box, and provide all the necessary infrastructure to get going quickly in any environment.

#### 🚧 System Requirements

Here are a few things you'll need globally available on your machine.

- [Python 3.8](https://www.python.org/)
- [asdf](https://asdf-vm.com/) (optional)

#### 🏎 Setup

The `cookiecutter` CLI needs to be installed locally. Follow the [installation docs here](https://cookiecutter.readthedocs.io/en/stable/installation.html) to get everything working. If you already have good python setup locally then `cookiecutter` is a quick `pip install cookiecutter` away.

Once `cookiecutter` is installed, you can use this template by cloning it locally, and then providing it as an argument to `cookiecutter`, or just use the direct Bitbucket link.

```bash
# provide cookiecutter with local template
cookiecutter flask-scaffold/

# use github uri directly
cookiecutter git@github.com:sammyteahan/cookiecutter-flask.git
```

#### Features

* Flask 2.3.2
* Docker
* gunicorn
* esbuild
* Tailwind
* Redis
* Celery
* flake8
* Black
* pytest
* Flask Extensions:
  * Flask-DB
  * Flask-SQLAlchemy
  * Flask-Secrets
  * Flask-Static-Digest
  * Flask-Marshmallow
  * Flask-Httpauth
  * Flask-Login
  * Flask-Mail
  * Flask-WTF
  * Flask-Debugtoolbar