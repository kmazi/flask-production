FROM python:3.12.1

# set app directory
ENV APP_HOME /app

# set working directory
WORKDIR $APP_HOME

# install dependencies
COPY requirements/base.txt requirements/base.txt
COPY requirements/dev.txt requirements/dev.txt
RUN pip install -r requirements/dev.txt

# copy app to container
COPY . ./

# start webserver on container startup
EXPOSE 8000

CMD ["flask", "--app", "flaskapp:create_app(env='dev')", "run", "--debug"]