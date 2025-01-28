# Docker Multi-Database Environment

A flexible Docker Compose environment to spin up multiple databases with **persistent storage**.  
Currently includes:
- [MySQL](https://hub.docker.com/_/mysql)
- [MongoDB](https://hub.docker.com/_/mongo)

Plans to add more in the future (e.g., PostgreSQL, Redis, etc.).  
Use this as a local development environment or testing sandbox.

## Features

- **Multiple Databases** under one `docker-compose.yml`
- **Named Volumes** for data persistence
- Credentials & ports easily overridden via `.env` variables
- Straightforward to **extend** with additional services

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)  
  *(Docker Desktop includes Docker Compose v2 by default.)*

## Getting Started

1. **Clone** this repository:
   
~~~bash
git clone https://github.com/<your-username>/docker-multi-db-env.git
cd docker-multi-db-env
~~~

2. **(Optional)** Copy `.env.example` to `.env` and adjust credentials/ports:

~~~bash
cp .env.example .env
# Then edit .env to match your desired configuration
~~~

3. **Start** the databases you need. For instance, to start **all** defined services:

~~~bash
docker-compose up -d
~~~

Or if you just want **MySQL** and **MongoDB**:

~~~bash
docker-compose up -d mysql mongodb
~~~

4. **Verify** the containers are running:

~~~bash
docker-compose ps
~~~

You should see `mysql` and `mongodb` in the `Up` state.

5. **Connect** to each database:

- **MySQL**  
  - Host: `localhost` (from host) or `mysql` (in Docker network)  
  - Port: `3306`  
  - User: `testuser`  
  - Password: `testpass`  
  - Database: `mydb`  

- **MongoDB**  
  - Host: `localhost` (from host) or `mongodb` (in Docker network)  
  - Port: `27017`  
  - User: `root`  
  - Password: `rootpass`  

6. **Stop** the containers when finished:

~~~bash
docker-compose down
~~~

This removes the containers but **retains** the named volumes, keeping your data intact.

---

## Adding More Databases

Feel free to add additional services in `docker-compose.yml`. For example, to add **PostgreSQL**, you might add:

~~~yaml
postgres:
  image: postgres:latest
  environment:
    - POSTGRES_USER=${POSTGRES_USER:-postgres}
    - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-postgrespass}
  ports:
    - "5432:5432"
  volumes:
    - postgres_data:/var/lib/postgresql/data
~~~

Then declare `postgres_data` in the volumes section:

~~~yaml
volumes:
  postgres_data:
~~~

---

## Data Persistence

This setup uses **named volumes** so your data persists across container recreations. For example:

- **MySQL** data is stored in `mysql_data` volume → `/var/lib/mysql`
- **MongoDB** data is stored in `mongodb_data` volume → `/data/db`

To completely remove **all** data, you can remove the volumes:

~~~bash
docker-compose down -v
~~~

*(This will delete the containers **and** the volumes, which erases all stored data.)*

---

## Contributing

- Report bugs or request features by opening an **issue**.
- Submit improvements via **pull requests**.

---
