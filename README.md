## Slow and Fast PostgreSQL Insertions

Benchmarking three different ways to insert data into PostgreSQL using psycopg library in Python.

## Run

This repository requires Python 3.10+, [Poetry](https://python-poetry.org/), and [Docker](https://www.docker.com/).

1. Install dependencies & get into the environment.

```sh
poetry install
poetry shell
```

2. In **a separate terminal window**, build and spin up PostgreSQL locally via Docker.

```sh
docker build -t customersdb .
docker run -d -p 5555:5432 customersdb
```

Run `docker ps` to verify that the container is running OK. It should give the following output:

```sh
CONTAINER ID   IMAGE         COMMAND                  CREATED         STATUS         PORTS                                       NAMES
<container-id>   customersdb   "docker-entrypoint.s…"   3 minutes ago   Up 3 minutes   0.0.0.0:5555->5432/tcp, :::5555->5432/tcp   adoring_galileo
```

3. In the original terminal window with the Python env, generate the data.

```sh
cd src
python generate_data.py
```

4. Run the benchmarking code.

```sh
python main.py
```