#FROM rockylinux:8
FROM python:3.11.5

# Install system stuff
RUN apt-get update

ENV PYTHON_VERSION 3.11.5
RUN wget --no-verbose https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz \
    && tar -C /usr/local/bin -xzvf Python-$PYTHON_VERSION.tgz \
    && rm Python-$PYTHON_VERSION.tgz \
    && cd /usr/local/bin/Python-$PYTHON_VERSION \
    && ./configure --enable-optimizations \
    && make altinstall

RUN ln -s /usr/local/bin/python3.11 /usr/bin/python \
 && ln -s /usr/local/bin/pip3.8 /usr/bin/pip

# Download and install dockerize.
ENV DOCKERIZE_VERSION v0.6.1
RUN wget --no-verbose https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# Set PYTHONUNBUFFERED so output is displayed in the Docker log
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.2.0

WORKDIR /usr/src/app

# Poetry commands reference https://python-poetry.org/docs/cli/#run
COPY pyproject.toml poetry.lock ./
RUN pip install --upgrade pip \
 && pip install poetry==$POETRY_VERSION \
 && poetry lock \
 && poetry export --without-hashes -f requirements.txt -o requirements.txt \
 && poetry export --dev --without-hashes -f requirements.txt -o requirements-dev.txt \
 && pip install -r requirements-dev.txt
