import csv
import psycopg

from timer import timeit

customers_data_filepath = "customers_data.csv"

def read_customer_data(file_name):
    with open(file_name, mode='r') as file:
        csv_reader = csv.reader(file)
        
        # Skip the header
        _ = next(csv_reader)
        
        # Read the CSV into a list of tuples
        rows = [tuple(row) for row in csv_reader]
    
    return rows

def reset_customer_table():
    print("Resetting the 'customer' table ...")
    with psycopg.connect("host=localhost dbname=customers user=admin password=admin port=5555") as conn:
        with conn.cursor() as cur:
            # Delete the data
            cur.execute("TRUNCATE TABLE customer;")
            print("\tTable 'customer' truncated.")

            # Update statistics for the SQL planner to generate efficient execution plans
            cur.execute("ANALYZE customer;")
            print("\tTable 'customer' had been ANALYZEed;")

            # Commit the changes
            conn.commit()
            print("\tTable 'customer' reset.")

@timeit
def very_slow_insert(customer_data):
    # Insert data using numerous separate 'INSERT' commands
    with psycopg.connect("host=localhost dbname=customers user=admin password=admin port=5555") as conn:
        with conn.cursor() as cur:
            for id, name, age in customer_data:
                cur.execute(
                    "INSERT INTO customer (id, name, age) VALUES (%s, %s, %s)", (id, name, age)
                )
                conn.commit()

@timeit
def slow_insert(customer_data):
    # Insert data using a single 'INSERT' command with a list of values passed directly to it
    with psycopg.connect("host=localhost dbname=customers user=admin password=admin port=5555") as conn:
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO customer (id, name, age) VALUES (%s, %s, %s)", customer_data
            )
            conn.commit()

@timeit
def fast_copy(customer_data):
    # Insert data using 'COPY' and pass by data row-by-row
    with psycopg.connect("host=localhost dbname=customers user=admin password=admin port=5555") as conn:
        with conn.cursor() as cur:
            with cur.copy("COPY customer (id, name, age) FROM STDIN") as copy:
                for customer_record in customer_data:
                    copy.write_row(customer_record)

if __name__ == "__main__":
    customer_data = read_customer_data(customers_data_filepath)
    
    insertion_functions = [
        very_slow_insert,
        slow_insert,
        fast_copy
    ]

    for insert_f in insertion_functions:
        # Reset the table before another type of insertion
        reset_customer_table()
        insert_f(customer_data)


