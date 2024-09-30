import csv
import random
from faker import Faker

from timer import timeit

# Initialize Faker, a library that will help generate fake data
fake = Faker()

# File name for the generated CSV
file_name = "customers_data.csv"

# Number of rows
num_rows = 10_000_000

def generate_customer_id():
    return random.randint(10**9, 10**10 - 1)

def generate_age():
    return random.randint(1, 100)

@timeit
def write_to_csv():
    inserted_ids = set()

    with open(file_name, mode='w') as file:
        writer = csv.writer(file)
        
        writer.writerow(["id", "name", "age"])

        while len(inserted_ids) < num_rows:
            customer_id = generate_customer_id()
            if customer_id not in inserted_ids:
                inserted_ids.add(customer_id)
                writer.writerow([customer_id, fake.name(), generate_age()])

if __name__ == "__main__":
    write_to_csv()
    print(f"CSV file with {num_rows} rows has been generated: {file_name}")