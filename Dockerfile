FROM python:3.9.4-slim-buster

LABEL maintainer="Vladyslav Krylasov <vladyslav.krylasov@gmail.com>"

# Install security upgrades
# See: https://pythonspeed.com/articles/security-updates-in-docker/
RUN apt-get update && apt-get -y upgrade

# Install supervisord required by daphne
RUN apt-get install -y supervisor

# create the app user
RUN groupadd --system user && \
	useradd -g user --create-home --shell /bin/bash user

# Linux envs
ENV APP="/app"
ENV HOME="/home/user"
ENV PATH="${PATH}:${HOME}/.local/bin"

# Python envs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONOPTIMIZE=1
ENV PYTHONUNBUFFERED=1
# https://pythonspeed.com/articles/python-c-extension-crashes/
ENV PYTHONFAULTHANDLER=1

WORKDIR ${APP}

COPY ./conf/requirements.txt ./conf/

# Create a dir for daphne sockets
RUN mkdir -p /run/daphne && chown -R user:user /run/daphne && chmod -R 755 /run/daphne

# Pick a not root user
RUN chown -R user:user ${APP} && chmod -R 744 ${APP}
USER user

# Upgrade pip and install packages
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
	python3 -m pip install --no-cache-dir -r ./conf/requirements.txt

COPY . .

EXPOSE 8000

CMD ["/bin/sh", "./conf/start-cmd.sh"]
