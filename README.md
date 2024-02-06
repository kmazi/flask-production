# flask-production
A starter kit for flask app. A boilerplate code for flask application.

## Docker Setup
Setup is divided into two sub groups:
 - One resource server setup where all server dependencies are setup on the same machine as the application server.
 - Multiple resource server setup where server dependencies are setup on different servers other than the application server.
 
 ### Requirements
 1. Install the latest docker engine.
 2. Install docker compose.
 3. Create a .env file in your root directory. Copy the content of .env_sample into your .env file. Edit file with accurate values.

### One Resource Server Setup
 - In your root folder (folder containing docker-compose.yaml file) run `docker-compose up -d [--build]` to start up the server service and it's dependencies. You could add the `--build` option to build the image if it doesn't exist.

### Multiple Resource Server Setup
 - Run `docker network create flaskproweb` to create a network for connecting containers.
 - Run `docker build --tag flaskpropgdb:0.1.0 --file docker/postgres/Dockerfile .` to build postgres database image.
 - Run `docker run --name flaskpropgdb --network flaskproweb -d --env-file .env flaskpropgdb:0.1.0` to start a postgres database container.
 - Run `docker build --tag flaskpro:0.1.0 --file docker/Dockerfile .` to build the application image.
 - Run `docker run --name flaskproapi --network flaskproweb --env-file .env -d flaskpro:0.1.0` to start up application server.
 - Run `docker build --tag nginxserver:0.1.0 --file docker/nginx/Dockerfile .` to build nginx image.
 - Run `docker run --name flaskpronginxserver --network flaskproweb -d --publish 8000:80 nginxserver:0.1.0` to start up nginx reverse proxy server.


    ### On Development Setup
     - Run `docker-compose --file dev.docker-compose.yml up [--build] -d` to optionally build and start the application and it's dependencies on local machine.
## System Setup
