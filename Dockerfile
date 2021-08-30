FROM python:latest
# set app directory
ENV APP_HOME /app
# set working directory
WORKDIR $APP_HOME
# copy app to container
COPY . ./
# install dependencies
RUN pip install -r requirements.txt
# start webserver on container startup
EXPOSE 8000

CMD gunicorn -b 0.0.0.0:8000 'flaskapp:create_app()'