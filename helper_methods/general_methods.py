import re
import string
from datetime import timedelta, datetime
from functools import wraps
from typing import Text, Dict, Any
import mysql.connector
from faker import Faker
import random
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

import queries_location

_fake = Faker()


def db_executor(query: str) -> list:
    # This executes the passed query
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


# Validators #
# This verifies if the user input is only digits and exactly 4 digits long
def is_valid_cnp(cnp: str) -> bool:
    return bool(re.match(r"^\d{4}$", cnp))


# This verifies the password is a minimal of 8 characters
def is_valid_password(password: str) -> bool:
    return bool(len(password) >= 8)


# This verifies the password is a minimal of 8 characters
def is_valid_account_number(account_number: str) -> bool:
    return bool(re.match(r"^\d{6}$", account_number))


def is_valid_transfer_amount(amount: float, cnp: str) -> bool:
    balance = queries_location.get_balance_by_cnp_query(cnp)
    return 0 <= (balance - int(amount))


# Made to handle the logout or break intents if it's for the first validation in a form, this is to handle a rasa
# special limitation
def handle_break_and_logout_special_intents(validation_func):
    @wraps(validation_func)
    async def wrapper(
            self,
            slot_value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        # If the previous intent was break_intent or login_intent, skip validation
        if tracker.latest_message['intent'].get('name') in ['break_intent', 'login_intent']:
            return {"requested_slot": None}

        # Proceed with the actual validation
        return await validation_func(self, slot_value, dispatcher, tracker, domain)

    return wrapper


# Mock APIs #
def mock_api_get_balance() -> int:
    # Simulate a random balance value from the mock API
    balance = 10000
    return balance


# General methods #
def generate_random_taxes():
    gas_tax = random.randint(50, 500)
    electricity_tax = random.randint(50, 500)
    water_tax = random.randint(50, 500)
    rent_tax = random.choice([200, 300, 500, 800])

    return gas_tax, electricity_tax, water_tax, rent_tax


def generate_random_credit_card_data(cnp):
    card_number = ''.join(random.choices(string.digits, k=16))
    card_type = random.choice(['Mastercard', 'Visa', 'Discover', 'Amex'])
    credit_limit = random.randint(1000, 10000)
    outstanding_amount = random.randint(0, credit_limit)
    due_date = _fake.date_between(start_date='+1m', end_date='+2y')

    return {
        'cnp': cnp,
        'card_number': card_number,
        'card_type': card_type,
        'credit_limit': credit_limit,
        'outstanding_amount': outstanding_amount,
        'due_date': due_date
    }


def get_random_surname():
    # List of some common surnames
    surnames = ['Smith', 'Johnson', 'Brown', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin']

    # Return a random surname from the list
    return random.choice(surnames)


def get_random_password():
    # Return a random password that doesn't include quotes or semicolons
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(8))
    return password


def generate_random_transaction(cnp):
    transaction_types = ['Bill Payment', 'Fund Transfer']
    targets = ['Rent', 'Gas', 'Electricity', 'Water', 'Account Transfer']

    transaction = {'cnp': cnp, 'transaction_type': random.choice(transaction_types), 'target': random.choice(targets),
                   'amount': random.randint(100, 10000)}

    return transaction


def get_random_name(names_list):
    return names_list[random.randint(0, len(names_list) - 1)]


def generate_random_user_data(cnp):
    # Data
    names = ["John", "James", "Michael", "William", "David", "Richard", "Joseph", "Charles", "Thomas", "Daniel"]
    surnames = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]

    # Generate data
    name = get_random_name(names)
    surname = get_random_name(surnames)
    age = random.randint(18, 80)
    password = ''.join([str(random.randint(0, 9)) for _ in range(8)])  # Create a 8 digit random password
    account_number = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # Create a 6 digit random account number
    registration_date = generate_random_date()
    balance = random.randint(0, 5000)  # Random balance between 0 and 5000

    return {
        'cnp': cnp,
        'name': name,
        'surname': surname,
        'age': age,
        'password': password,
        'account_number': account_number,
        'registration_date': registration_date,
        'balance': balance
    }


def generate_random_date():
    start_date = datetime.now() - timedelta(days=365)  # One year ago
    random_date = start_date + timedelta(
        seconds=random.randint(0, int((datetime.now() - start_date).total_seconds())),
    )

    return random_date.strftime("%Y-%m-%d %H:%M:%S")  # Format it as MySQL datetime
