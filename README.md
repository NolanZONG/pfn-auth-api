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

## Usage
This project was tested successfully on 
- Ubuntu 24.04 LTS
- Docker version 28.0.0, build f9ced58
- Docker Compose version v2.33.0

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

## Todo and Improvement
This is just a prototype implementation due to the **time limitation**. 
If the goal is to make it production-ready, at least the following parts are needed:

- Add unit tests for each module and improve test coverage.
- Improve the comments to make the generated Open API doc clearly.
- The sensitive data are stored in a separate configuration file called `.env` currently, this should be sufficient and enough for development purposes, but we can consider use a secure secrets management tool in production
- Implement a service layer(e.g. `service.py`) to make the code structure clearer.
- Currently, the application is simply deployed on a single server. But I think the API performance requirements should be clarified before implementation, and then the code can be optimized accordingly, including infrastructure decisions.
- Use tools like Terraform to manage infrastructure as code.
- Integrate appropriate monitoring tools.

In addition, if possible, the API design itself may have room for improvement, which can be discussed in more detail.
