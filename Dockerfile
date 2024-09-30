# Use PostgreSQL 17 alpine image as the base
FROM postgres:17-alpine3.20

# Set environment variables for PostgreSQL
ENV POSTGRES_DB=customers \
    POSTGRES_USER=admin \
    POSTGRES_PASSWORD=admin

# Copy the SQL file to a folder inside the container
COPY ./src/customers.sql /docker-entrypoint-initdb.d/

# Expose the PostgreSQL default port
EXPOSE 5432