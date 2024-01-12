# flask-production
A starter kit for flask app

## Docker Setup
Setup is divided into two sub groups:
 - One resource server setup where all server dependencies are setup on the same machine as the application server.
 - Multiple resource server setup where server dependencies are setup on different servers other than the application server.
 
### One Resource Server Setup
### Multiple Resource Server Setup
 - Run `docker network create flaskproweb` to create a network for connecting containers.
 - Run `docker build --tag flaskpropgdb:0.1.0 --file docker/postgres/Dockerfile .` to build postgres database image.
 - Run `docker run --name flaskpropgdb --network flaskproweb -d --env-file .env flaskpropgdb:0.1.0` to start a postgres database container.
 - Run `docker build --tag flaskpro:0.1.0 --file docker/Dockerfile .` to build the application image.
 - Run `docker run --name flaskproapi --network flaskproweb --env-file .env -d flaskpro:0.1.0` to start up application server.
 - Run `docker run --name flaskpronginxserver --network flaskproweb -d --publish 8000:80 nginxserver:0.1.0` to start up nginx reverse proxy server.
## System Setup
