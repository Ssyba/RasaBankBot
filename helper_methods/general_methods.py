import asyncio
import re
from functools import wraps
from typing import Text, Dict, Any
import mysql.connector
from faker import Faker
import random
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
import queries_location

_fake = Faker()


# For database use #
def generate_random_user_data(cnp):
    # This creates the data that will be used to populate the data with a mock user
    cnp = cnp
    name = _fake.first_name()
    surname = _fake.last_name()
    age = random.randint(18, 100)
    password = "12345678"
    account_number = f"{random.randint(100000, 999999)}"
    registration_date = _fake.date_between(start_date='-5y', end_date='today')
    balance = random.randint(0, 1000000)

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
    return bool(len(account_number) == 6)


def is_valid_transfer_amount(amount: float, cnp: str) -> bool:
    balance = queries_location.get_balance_by_cnp_query(cnp)
    return 0 <= (balance - int(amount))


def mock_api_get_balance() -> int:
    # Simulate a random balance value from the mock API
    balance = 10000
    return balance


# Wrappers #
def skip_validate_if_logged_in(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        action, slot_value, dispatcher, tracker, domain = args
        logged_in_status = tracker.get_slot('logged_in_status_slot')
        if logged_in_status:
            return {"requested_slot": None}

        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return wrapper


def skip_validate_if_logged_out(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        action, slot_value, dispatcher, tracker, domain = args
        logged_in_status = tracker.get_slot('logged_in_status_slot')
        if not logged_in_status:
            return {"requested_slot": None}

        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return wrapper


def only_works_if_logged_out(func):
    @wraps(func)
    async def wrapper(action, dispatcher, tracker, domain):
        logged_in_status = tracker.get_slot('logged_in_status_slot')
        if logged_in_status:
            dispatcher.utter_message(text="Invalid operation because you are logged in.")
            return []

        if asyncio.iscoroutinefunction(func):
            return await func(action, dispatcher, tracker, domain)
        else:
            return func(action, dispatcher, tracker, domain)

    return wrapper


def only_works_if_logged_in(func):
    @wraps(func)
    async def wrapper(action, dispatcher, tracker, domain):
        logged_in_status = tracker.get_slot('logged_in_status_slot')
        if not logged_in_status:
            dispatcher.utter_message(text="Invalid operation because you are not logged in.")
            return []

        if asyncio.iscoroutinefunction(func):
            return await func(action, dispatcher, tracker, domain)
        else:
            return func(action, dispatcher, tracker, domain)

    return wrapper


def handle_break_and_logout_special_intents(validation_func):
    @wraps(validation_func)
    async def wrapper(
            self,
            slot_value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        # Extract the first slot name from the validation function name
        first_slot_name = validation_func.__name__.replace("validate_", "")

        # If the previous intent was break_intent or login_intent, skip validation
        if tracker.latest_message['intent'].get('name') in ['break_intent', 'login_intent']:
            return {first_slot_name: None}

        # Proceed with the actual validation
        return await validation_func(self, slot_value, dispatcher, tracker, domain)

    return wrapper
