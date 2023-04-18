from datetime import datetime
from general_methods import db_executor, generate_random_user_data, mock_api_get_balance
import random


# Create tables
def create_users_table_query():
    return db_executor(
        "CREATE TABLE users ("
        "id INT AUTO_INCREMENT PRIMARY KEY, "
        "CNP VARCHAR(4) UNIQUE, "
        "name VARCHAR(255), "
        "surname VARCHAR(255), "
        "age INT(2), "
        "password VARCHAR(255), "
        "account_number VARCHAR(6) UNIQUE, "
        "registration_date DATE, "
        "balance INT)"
    )


def create_bills_table_query():
    return db_executor(
        "CREATE TABLE bills ("
        "id INT AUTO_INCREMENT PRIMARY KEY, "
        "cnp VARCHAR(4) UNIQUE, "
        "gas INT, "
        "electricity INT, "
        "water INT, "
        "rent INT)"
    )


# Update tables
def delete_users_table_query():
    return db_executor("DROP TABLE users")


def delete_bills_table_query():
    return db_executor("DROP TABLE bills")


def clear_data_users_table_query():
    query = "TRUNCATE TABLE users"
    db_executor(query)


def clear_data_bills_table_query():
    query = "TRUNCATE TABLE bills"
    db_executor(query)


def fill_bills_table_query():
    # Select CNPs from the users table
    users_table_cnps = [cnp[0] for cnp in db_executor("SELECT CNP FROM users")[0]]
    bills_table_cnps = [cnp[0] for cnp in db_executor("SELECT CNP FROM bills")[0]]

    for cnp in users_table_cnps:
        if cnp not in bills_table_cnps:
            gas = random.randint(50, 500)
            electricity = random.randint(50, 500)
            water = random.randint(50, 500)
            rent = random.choice([200, 300, 500, 800])

            query = (
                f"INSERT INTO bills (cnp, gas, electricity, water, rent) "
                f"VALUES ('{cnp}', {gas}, {electricity}, {water}, {rent})"
            )
            db_executor(query)
        else:
            print(f"CNP '{cnp}' already exists in bills table, skipping...")


def add_new_user_query(cnp: str, name: str, surname: str, age: str, password: str):
    # Generate the registration date
    registration_date = datetime.now().strftime("%Y-%m-%d")

    # Get the balance from the mock API
    balance = mock_api_get_balance()

    # Get the last user's ID and increment it
    last_user_id_result = db_executor("SELECT id FROM users ORDER BY id DESC LIMIT 1")
    last_user_id = last_user_id_result[0][0]  # Extract the last_user_id value
    new_user_id = int(last_user_id) + 1

    # Generate the account number using the new user ID
    account_number = str(new_user_id).zfill(6)

    # Execute the INSERT query to add the new user to the table
    insert_query = f"""INSERT INTO users (
        id, CNP, name, surname, age, password, registration_date, balance, account_number
    ) VALUES (
        {new_user_id}, '{cnp}', '{name}', '{surname}', '{age}', '{password}', '{registration_date}', {balance}, 
        '{account_number}'
    )"""
    db_executor(insert_query)


def delete_user_by_cnp_query(cnp: str) -> None:
    delete_query = f"DELETE FROM users WHERE CNP='{cnp}'"
    db_executor(delete_query)


def insert_random_user_query(cnp):
    user = generate_random_user_data(cnp)
    insert_query = f"""
        INSERT INTO users (CNP, name, surname, age, password, account_number, registration_date, balance)
        VALUES (
            '{user['cnp']}',
            '{user['name']}',
            '{user['surname']}',
            '{user['age']}',
            '{user['password']}',
            '{user['account_number']}',
            '{user['registration_date']}',
            '{user['balance']}'
        )
    """
    db_executor(insert_query)


def transfer_funds_query(sender_cnp: str, recipient_account_number: str, transfer_amount: float) -> None:
    transfer_query = f"""
        BEGIN;
            UPDATE users SET balance = balance - {transfer_amount} WHERE CNP='{sender_cnp}';
            UPDATE users SET balance = balance + {transfer_amount} WHERE account_number='{recipient_account_number}';
        COMMIT;
    """
    db_executor(transfer_query)


# Find inside tables
def find_user_by_cnp_query(cnp: str) -> dict:
    # Get the row data and column names
    row_data, column_names = db_executor("SELECT * FROM users WHERE CNP = '%s'" % cnp)

    # If there is a result, convert it to a dictionary
    if row_data:
        user = dict(zip(column_names, row_data[0]))
        return user
    else:
        return {}


def find_bills_by_cnp_query(cnp: str) -> dict:
    # Get the row data and column names
    row_data, column_names = db_executor("SELECT * FROM bills WHERE CNP = '%s'" % cnp)

    # If there is a result, convert it to a dictionary
    if row_data:
        bills = dict(zip(column_names, row_data[0]))
        return bills
    else:
        return {}


def find_user_name_by_cnp_query(cnp: str) -> list:
    return db_executor("SELECT name FROM users WHERE cnp = '%s'" % cnp)


def find_user_by_account_number_query(account_number: str) -> dict:
    # Get the row data and column names
    row_data, column_names = db_executor("SELECT * FROM users WHERE account_number = '%s'" % account_number)

    # If there is a result, convert it to a dictionary
    if row_data:
        user = dict(zip(column_names, row_data[0]))
        return user
    else:
        return {}


def get_account_number_by_cnp(cnp: str) -> str:
    account_number_query = f"SELECT account_number FROM users WHERE CNP='{cnp}'"
    result = db_executor(account_number_query)

    return result[0][0][0]


def get_balance_by_cnp_query(cnp: str) -> int:
    balance_query = f"SELECT balance FROM users WHERE CNP='{cnp}'"
    result = db_executor(balance_query)

    return result[0][0][0]
