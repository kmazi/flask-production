# define an alias for the specific python version used in this file.
FROM python:3.12.1-slim-bookworm as python

# Python build stage
FROM python as python-build-stage

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential

# Requirements are copied here to ensure they will be cached.
COPY requirements/base.txt ./requirements/base.txt
COPY requirements/prod.txt ./requirements/prod.txt
COPY requirements.txt .

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --wheel-dir /usr/src/app/wheels  \
  -r requirements.txt


# Python 'run' stage
FROM python as python-run-stage

ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV production

WORKDIR ${APP_HOME}

RUN addgroup --system flask \
    && adduser --system --ingroup flask flask

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  # Translations dependencies
  gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

# use wheels to install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

# make flask owner of the WORKDIR directory as well.
RUN chown -R flask:flask ${APP_HOME}

RUN chmod -R o+w /app/

USER flask

# Copy app folder and dependencies
COPY flaskapi flaskapi
COPY instance instance
COPY gunicorn.conf.py .
COPY docker/flask/entrypoint .

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint"]

CMD [ "gunicorn", "flaskapi:create_app()" ]
