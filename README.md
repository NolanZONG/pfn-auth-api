# Coding Test Project

This is a prototype of the PFN coding test assignment, which is to implement an authentication server. 

It is implemented in Python 3.12 and integrated with a MySQL 8.0 database.


## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/lo/) - A modern, fast (high-performance), web framework for building APIs. 
I chose it because it is easy to learn, fast to code, and good for prototyping. 
- [Uvicorn](https://www.uvicorn.org/) - An ASGI web server implementation for Python.
- [Pydantic](https://docs.pydantic.dev/latest/) - Data validation library. It is used for validating query parameters.
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM toolkit for SQL. It can help me handle the interaction with the DB, 
allowing me to focus on business logic.

## Directory structure:
```
pfn-auth-api/
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── README.md
├── requirements.txt
└── auth_api/
      └── auth.py
      └── database.py
      └── main.py
      └── model.py
      └── repository.py
      └── validator.py
```
- auth.py: provides a http basic authentication module
- database.py: sets up the configuration for connecting to a MySQL database
- main.py: implements a FastAPI application
- model.py: defines an SQLAlchemy model for storing user auth data
- repository.py: provides a repository for the CRUD of user auth data
- validator.py: defines the validators for validating query parameters


### Secrets management
#### Development Environment

The API key and other sensitive data are stored in a separate configuration file called `.env`, 
which is specific to the development environment. This file should not be committed to version control systems. 
The application code retrieves the password from the environment variable. 
This approach allows for easy configuration and avoids exposing passwords in the code. 
I believe this is sufficient for development purposes.

#### Production Environment
We can consider use a secure secrets management system, for example:
- [HashiCorp Vault](https://www.hashicorp.com/products/vault)
- [AWS Secrets Manager](https://aws.amazon.com/jp/secrets-manager/)
- [GCP Secrets Manager](https://cloud.google.com/secret-manager)

These tools provide secure storage and retrieval of sensitive data, including api_key, passwords. 
Access to the secrets can be tightly controlled, and the passwords can be rotated regularly for enhanced security.

## Usage
This project was tested successfully on 
- Ubuntu 24.04 LTS
- Docker version 20.10.14, build a224086
- docker-compose version 1.29.2, build 5becea4c

You can run it on your local environment by following these steps:


1. Go to the project folder `cd pfn-auth-api`
2. Copy the `.env.example` and rename it to `.env` and put it in the same directory of `.env.example`.
Fill in the config variable in the `.env`:
```
MYSQL_PASSWORD: any value you preferred
MYSQL_ROOT_PASSWORD: any value you preferred
HTTP_PORT: port number for http service, you can use any available port on your local environment.
HTTP_PROXY/HTTPS_PROXY: Optional. Fill in it if you are behind a proxy.
```
You can also change the `MYSQL_USERNAME` to any other value you preferred.

3. Run the command
   ```
   docker-compose up -d
   ```
   
4. If all goes well, the app is ready now.
```shell
zongnan@fastapi:~/pfn-auth-api$ docker compose ps
NAME           IMAGE              COMMAND                  SERVICE   CREATED          STATUS                    PORTS
auth_api_app   pfn-auth-api-app   "uvicorn auth_api.ma…"   app       37 seconds ago   Up 6 seconds              0.0.0.0:80->80/tcp, :::80->80/tcp
auth_api_db    mysql:8.0          "docker-entrypoint.s…"   db        38 seconds ago   Up 37 seconds (healthy)   3306/tcp, 33060/tcp
```

5. You can send requests from the browser or `curl`. 
You can also find the auto-generated API documentation on `http://{domain}:{port}/docs`

6. You can use `docker-compose down` to stop and remove the service
