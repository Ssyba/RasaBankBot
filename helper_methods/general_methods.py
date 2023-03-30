import mysql.connector
from faker import Faker
import random

fake = Faker()


# This creates the data that will be used to populate the data with a mock user
def generate_random_user(cnp):
    cnp = cnp
    name = fake.first_name()
    surname = fake.last_name()
    age = random.randint(18, 100)
    password = "12345678"
    account_number = f"{random.randint(100000, 999999)}"
    register_date = fake.date_between(start_date='-5y', end_date='today')
    balance = random.randint(0, 1000000)

    return {
        'cnp': cnp,
        'name': name,
        'surname': surname,
        'age': age,
        'password': password,
        'account_number': account_number,
        'register_date': register_date,
        'balance': balance
    }


# This executes the passed query
def db_executor(query: str) -> list:
    # Create connection to the MySQL server
    db_connection = mysql.connector.connect(
        host="localhost",
        user="marius",
        password="1111",
        database="mydatabase"
    )

    # Create a cursor object to execute SQL queries
    cursor = db_connection.cursor()

    # Execute the query
    cursor.execute(query)

    # Check if the query requires commit
    query_type = query.split(maxsplit=1)[0].upper()
    if query_type in ["CREATE", "INSERT", "UPDATE", "DELETE", "COMMIT", "ROLLBACK", "SAVEPOINT", "SET TRANSACTION"]:
        # Commit the changes
        db_connection.commit()
        result = None
    else:
        # Fetch the results
        result = cursor.fetchall()

        # Fetch the column names if available
        if cursor.description is not None:
            column_names = [desc[0] for desc in cursor.description]
            result = [result, column_names]

    # Close the cursor and database connection
    cursor.close()
    db_connection.close()

    return result
