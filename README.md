# Docker Multi-Database Environment + FastAPI

A flexible Docker Compose environment to spin up **multiple databases** with **persistent storage**, plus a **FastAPI** application (managed by **Poetry**) providing **generic CRUD** endpoints for MySQL and MongoDB.

## Features

- **MySQL** and **MongoDB** containers with named volumes for data persistence  
- **FastAPI** app for generic CRUD operations  
- **Poetry** for Python dependency management  
- Easy to **extend** with more databases/services and additional endpoints  

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)  
  *(Docker Desktop includes Docker Compose v2 by default)*
- [Poetry](https://python-poetry.org/docs/) (for local Python dependency management)

## Getting Started

1. **Clone** this repository:
   
   ~~~bash
   git clone https://github.com/<your-username>/docker-multi-db-env.git
   cd docker-multi-db-env
   ~~~

2. **(Optional)** Copy `.env.example` to `.env` and adjust credentials:
   
   ~~~bash
   cp .env.example .env
   # Then edit .env to match your desired configuration
   ~~~

3. **Start** the databases (MySQL, MongoDB):
   
   ~~~bash
   docker-compose up -d
   ~~~
   
   This creates and starts the containers. Check with:
   
   ~~~bash
   docker-compose ps
   ~~~
   
   Both `mysql` and `mongodb` should be `Up`.

4. **Install** Python dependencies with Poetry:
   
   ~~~bash
   poetry install
   ~~~
   
   This installs **FastAPI**, **SQLAlchemy**, **PyMongo**, etc.

5. **Run** the FastAPI app (still in your project root):
   
   ~~~bash
   poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ~~~
   
   The API should be reachable at [http://localhost:8000](http://localhost:8000).  
   Explore the auto-generated docs at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## Defining Your Own MySQL Schema with SQL Files

You can define your **own database schema** by placing `.sql` files inside the **`mysql-init-scripts/`** directory.

### **How It Works**
- Any `.sql` file inside `mysql-init-scripts/` **will be executed** when the MySQL container starts.
- This allows you to **automate table creation** or insert default data.

### **Steps to Add Your Own Schema**
1. **Create an SQL file** inside `mysql-init-scripts/`.  
   Example: `mysql-init-scripts/my_schema.sql`
   
   ~~~sql
   CREATE TABLE user (
       id VARCHAR(255) NOT NULL PRIMARY KEY,
       username VARCHAR(255) NOT NULL,
       email VARCHAR(255) NOT NULL,
       name VARCHAR(255) NOT NULL,
       is_active TINYINT(1) NOT NULL
   );
   ~~~

2. **Restart the MySQL container** so it picks up the changes:

   ~~~bash
   docker-compose down
   docker-compose up -d
   ~~~

3. **Verify the schema is applied**:

   ~~~bash
   docker exec -it mysql mysql -u root -p mydb
   SHOW TABLES;
   ~~~

---

## Usage

- **MySQL** endpoints:
  - `GET /mysql/{table_name}` → Retrieve all rows
  - `POST /mysql/{table_name}` → Insert a row (send JSON body)
  - `PUT /mysql/{table_name}/{id}` → Update a row by ID
  - `DELETE /mysql/{table_name}/{id}` → Delete a row by ID
- **MongoDB** endpoints:
  - `GET /mongo/{collection_name}` → Retrieve all documents
  - `POST /mongo/{collection_name}` → Insert a document
  - `PUT /mongo/{collection_name}/{doc_id}` → Update a document by `_id`
  - `DELETE /mongo/{collection_name}/{doc_id}` → Delete a document by `_id`

---

## Adding More Databases

To add, for example, **PostgreSQL**:
1. Add a `postgres` service in `docker-compose.yml`:

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

2. Declare `postgres_data` in the volumes section:

   ~~~yaml
   volumes:
     postgres_data:
   ~~~

3. Create a `postgres.py` in `app/dependencies/` for the connection.  
4. Create a `postgres_generic.py` router for generic CRUD, if desired.  

---

## Data Persistence

Named volumes ensure data persists across container restarts:
- **mysql_data** → `/var/lib/mysql`
- **mongodb_data** → `/data/db`

To **wipe** all data:
~~~bash
docker-compose down -v
~~~
(This removes both containers **and** volumes.)

---

## Contributing

- Open an **issue** for bugs or feature requests.
- Submit **pull requests** for improvements.
