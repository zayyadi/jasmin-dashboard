# ###########
# # BUILDER #
# ###########

# # pull official base image
# FROM python:3.11.4-slim-buster as builder

# # set work directory
# WORKDIR /usr/src/app

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # install system dependencies
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends gcc

# # lint
# RUN pip install --upgrade pip
# # RUN pip install flake8==6.0.0
# COPY . /usr/src/app/
# # RUN flake8 --ignore=E501,F401 .

# # install python dependencies
# COPY ./requirements.txt .
# RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


# #########
# # FINAL #
# #########

# # pull official base image
# FROM python:3.11.4-slim-buster

# # create directory for the app user
# RUN mkdir -p /home/app

# # create the app user
# RUN addgroup --system app && adduser --system --group app

# # create the appropriate directories
# ENV HOME=/home/app
# ENV APP_HOME=/home/app/web
# RUN mkdir $APP_HOME
# RUN mkdir $APP_HOME/staticfiles
# RUN mkdir $APP_HOME/mediafiles
# RUN mkdir -p /home/app/web/logs && chown -R app:app /home/app/web/logs
# WORKDIR $APP_HOME

# # install dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends netcat
# COPY --from=builder /usr/src/app/wheels /wheels
# COPY --from=builder /usr/src/app/requirements.txt .
# RUN pip install --upgrade pip
# RUN pip install --no-cache /wheels/*

# # copy entrypoint.prod.sh
# COPY ./entrypoint.sh .
# RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
# RUN chmod +x  $APP_HOME/entrypoint.sh

# # copy project
# COPY . $APP_HOME

# # chown all the files to the app user
# RUN chown -R app:app $APP_HOME

# # change to the app user
# USER app

# # run entrypoint.prod.sh
# ENTRYPOINT ["/home/app/web/entrypoint.sh"]

# Builder Stage
FROM python:3.10-slim as builder

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

RUN pip install --upgrade pip 

COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

# Final Image
FROM python:3.10-slim

RUN mkdir -p /home/app

RUN groupadd -r app && useradd --no-log-init -r -g app app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir -p $APP_HOME/logs  # Ensure the logs directory is created
WORKDIR $APP_HOME

RUN apt-get update && apt-get install -y libpq-dev
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt ./
RUN pip install --no-cache /wheels/*

# Copy entrypoint script
COPY ./entrypoint.sh $APP_HOME/entrypoint.sh
RUN chmod +x $APP_HOME/entrypoint.sh

COPY . $APP_HOME

# Ensure the app user has ownership of the logs directory
RUN chown -R app:app $APP_HOME/logs

RUN chown -R app:app $APP_HOME

USER app

# Set the entrypoint
ENTRYPOINT ["./entrypoint.sh"]