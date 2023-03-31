from datetime import datetime

from general_methods import db_executor, generate_random_user


def create_users_table_query():
    return db_executor(
        "CREATE TABLE users ("
        "id INT AUTO_INCREMENT PRIMARY KEY, "
        "CNP VARCHAR(4), "
        "name VARCHAR(255), "
        "surname VARCHAR(255), "
        "age INT(2), "
        "password VARCHAR(255), "
        "account_number VARCHAR(6), "
        "registration_date DATE, "
        "balance INT)"
    )


def delete_users_table_query():
    return db_executor("DROP TABLE users")


def find_user_by_cnp_query(cnp: str) -> dict:
    # Get the row data and column names
    row_data, column_names = db_executor("SELECT * FROM users WHERE CNP = '%s'" % cnp)

    # If there is a result, convert it to a dictionary
    if row_data:
        user = dict(zip(column_names, row_data[0]))
        return user
    else:
        return None


def find_user_name_by_cnp_query(cnp: str) -> str:
    return db_executor("SELECT name FROM users WHERE cnp = '%s'" % cnp)


def add_new_user(cnp: str, name: str, surname: str, age: str, password: str) -> list:
    # Generate the registration date
    registration_date = datetime.now().strftime("%Y-%m-%d")

    # Get the balance from the mock API
    balance = mock_api_get_balance()

    # Get the last user's ID and increment it
    last_user_id_result = db_executor("SELECT id FROM users ORDER BY id DESC LIMIT 1")
    last_user_id = last_user_id_result[0][0]  # Extract the last_user_id value
    new_user_id = int(last_user_id[0]) + 1

    # Generate the account number using the new user ID
    account_number = str(new_user_id).zfill(6)

    # Execute the INSERT query to add the new user to the table
    insert_query = f"""INSERT INTO users (
        id, CNP, name, surname, age, password, registration_date, balance, account_number
    ) VALUES (
        {new_user_id}, '{cnp}', '{name}', '{surname}', '{age}', '{password}', '{registration_date}', {balance}, '{account_number}'
    )"""
    db_executor(insert_query)  # Assume this method executes the given SQL query on the database


def mock_api_get_balance() -> int:
    # Simulate a random balance value from the mock API
    balance = 10000
    return balance


def add_new_user(cnp: str, name: str, surname: str, age: str, password: str) -> list:
    # generate the registration date
    registration_date = datetime.now().strftime("%Y-%m-%d")

    # get the balance from the mock API
    balance = mock_api_get_balance()

    # Get the last user ID
    last_user_id_result = db_executor("SELECT id FROM users ORDER BY id DESC LIMIT 1")
    last_user_id = last_user_id_result[0][0] if last_user_id_result else 0

    # Increment the last user ID and generate the account number
    new_user_id = int(last_user_id[0]) + 1
    account_number = str(new_user_id).zfill(6)

    # execute the INSERT query to add the new user to the table
    insert_query = f"INSERT INTO users (id, CNP, name, surname, age, password, registration_date, balance, account_number) " \
                   f"VALUES ({new_user_id}, '{cnp}', '{name}', '{surname}', '{age}', '{password}', '{registration_date}', {balance}, '{account_number}')"
    db_executor(insert_query)  # assume this method executes the given SQL query on the database


def delete_user_by_cnp(cnp: str) -> None:
    delete_query = f"DELETE FROM users WHERE CNP='{cnp}'"
    db_executor(delete_query)  # assume this method executes the given SQL query on the database


def get_balance_by_cnp(cnp: str) -> int:
    balance_query = f"SELECT balance FROM users WHERE CNP='{cnp}'"
    result = db_executor(balance_query)  # assume this method executes the given SQL query on the database
    print("potato", result)

    return result[0][0][0]


def update_login_status(cnp: str, login_status: bool) -> None:
    update_query = f"UPDATE users SET login_status={int(login_status)} WHERE CNP='{cnp}'"
    db_executor(update_query)


def insert_random_user(cnp):
    user = generate_random_user(cnp)
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
