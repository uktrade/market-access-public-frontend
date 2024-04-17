# #Using non standard build to enable Playwright tests
FROM mcr.microsoft.com/playwright/python:v1.39.0-jammy

# Install system stuff
# RUN apt-get update
# RUN apt-get install -y build-essential python3-dev python3.9 python3-pip libffi-dev libmagic-dev locales locales-all


# Install Python 3.9 and other system dependencies
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip \
    libevent-2.1-7 \
    libffi-dev \
    libmagic-dev \
    locales \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# RUN dnf -y update \
#  && dnf -y install \
#     gcc \
# 	wget \
#     postgresql \
#     # packages so python can be compiled
# 	nano \
# 	make \
# 	which \
#     openssl-devel \
#     bzip2-devel \
# 	zlib-devel \
#     libffi \
# 	libffi-devel \
#     # packages for pytest
#     sqlite-devel \
#     # packages for localdef
#     glibc-locale-source \
#     glibc-langpack-en \
#     # packages for ssh server
#     openssh-server \
#     openssh-clients \
#  && dnf -y clean all \
#  && rm -rf /var/cache/dnf

# ENV PYTHON_VERSION 3.9.17
# RUN wget --no-verbose https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz \
#     && tar -C /usr/local/bin -xzvf Python-$PYTHON_VERSION.tgz \
#     && rm Python-$PYTHON_VERSION.tgz \
#     && cd /usr/local/bin/Python-$PYTHON_VERSION \
#     && ./configure --enable-optimizations \
#     && make altinstall

# RUN ln -s /usr/local/bin/python3.9 /usr/bin/python \
#  && ln -s /usr/local/bin/pip3.9 /usr/bin/pip

# SSH
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
    systemd-tmpfiles-setup.service ] || rm -f $i; done); \
    rm -f /lib/systemd/system/multi-user.target.wants/*;\
    rm -f /etc/systemd/system/*.wants/*;\
    rm -f /lib/systemd/system/local-fs.target.wants/*; \
    rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
    rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
    rm -f /lib/systemd/system/basic.target.wants/*;\
    rm -f /lib/systemd/system/anaconda.target.wants/*;
VOLUME [ "/sys/fs/cgroup" ]
RUN echo root:pass | chpasswd
CMD ["/usr/sbin/sshd", "-D"]

# Download and install dockerize.
ENV DOCKERIZE_VERSION v0.6.1
RUN curl -sLO https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# Set locale to en GB
RUN localedef -c -i en_GB -f UTF-8 en_GB.UTF-8
ENV LANG en_GB.utf-8
ENV LC_ALL en_GB.utf-8

# Set PYTHONUNBUFFERED so output is displayed in the Docker log
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.6.1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=200 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Create a symlink for python if it doesn't already exist
RUN if [ ! -f /usr/bin/python ]; then \
        ln -s /usr/bin/python3.9 /usr/bin/python; \
    fi


WORKDIR /usr/src/app

# Poetry commands reference https://python-poetry.org/docs/cli/#run
COPY pyproject.toml poetry.lock ./
RUN pip install --upgrade pip \
 && pip install poetry==$POETRY_VERSION \
 && poetry export --without-hashes -f requirements.txt -o requirements.txt \
 && poetry export --dev --without-hashes -f requirements.txt -o requirements-dev.txt \
 && pip install -r requirements-dev.txt

 # Set up Playwright
RUN playwright install
RUN playwright install-deps
