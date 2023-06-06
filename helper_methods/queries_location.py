from datetime import datetime
from general_methods import db_executor, generate_random_user_data, mock_api_get_balance, generate_random_taxes, \
    generate_random_credit_card_data
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


def create_transactions_table_query():
    return db_executor(
        "CREATE TABLE transactions ("
        "id INT AUTO_INCREMENT PRIMARY KEY, "
        "CNP VARCHAR(4), "
        "transaction_type VARCHAR(255), "
        "target VARCHAR(255), "
        "amount INT, "
        "transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    )


def create_credit_cards_table_query():
    return db_executor(
        "CREATE TABLE credit_cards ("
        "id INT AUTO_INCREMENT PRIMARY KEY, "
        "CNP VARCHAR(4), "
        "card_number VARCHAR(16), "
        "card_type VARCHAR(255), "
        "credit_limit INT, "  # Changed column name from limit to credit_limit
        "outstanding_amount INT, "
        "due_date DATE)"
    )


# Update tables
# Delete tables
def delete_users_table_query():
    return db_executor("DROP TABLE users")


def delete_bills_table_query():
    return db_executor("DROP TABLE bills")


def delete_transactions_table_query():
    return db_executor("DROP TABLE transactions")


def delete_credit_cards_table_query():
    return db_executor("DROP TABLE IF EXISTS credit_cards")


def clear_data_users_table_query():
    query = "TRUNCATE TABLE users"
    db_executor(query)


# Clear data from tables
def clear_data_bills_table_query():
    query = "TRUNCATE TABLE bills"
    db_executor(query)


def clear_data_transactions_table_query():
    query = "TRUNCATE TABLE transactions"
    db_executor(query)


def clear_credit_cards_table_query():
    return db_executor("DELETE FROM credit_cards")


def fill_bills_table_query():
    # Select CNPs from the users table
    users_table_cnps = [cnp[0] for cnp in db_executor("SELECT CNP FROM users")[0]]
    bills_table_cnps = [cnp[0] for cnp in db_executor("SELECT CNP FROM bills")[0]]

    for cnp in users_table_cnps:
        if cnp not in bills_table_cnps:
            gas, electricity, water, rent = generate_random_taxes()

            query = (
                f"INSERT INTO bills (cnp, gas, electricity, water, rent) "
                f"VALUES ('{cnp}', {gas}, {electricity}, {water}, {rent})"
            )
            db_executor(query)
        else:
            print(f"CNP '{cnp}' already exists in bills table, skipping...")


def update_bills_table_with_random_taxes_query() -> None:
    update_bills_query = """
        UPDATE bills
        SET gas = gas + %s, electricity = electricity + %s, water = water + %s, rent = rent + %s;
    """

    gas_tax, electricity_tax, water_tax, rent_tax = generate_random_taxes()

    db_executor(update_bills_query % (gas_tax, electricity_tax, water_tax, rent_tax))


def add_new_user_query(cnp: str, name: str, surname: str, age: str, password: str):
    # Generate the registration date
    registration_date = datetime.now().strftime("%Y-%m-%d")

    # Get the balance from the mock API
    balance = mock_api_get_balance()

    # Get the last user's ID and increment it
    last_user_id_result = db_executor("SELECT id FROM users ORDER BY id DESC LIMIT 1")
    last_user_id = last_user_id_result[0][0][0]  # Extract the last_user_id value
    new_user_id = last_user_id + 1

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


# Insert data in tables
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


def insert_random_credit_card_query(cnp):
    for _ in range(random.randint(0, 3)):  # Generating 0 to 3 credit cards for each user
        credit_card = generate_random_credit_card_data(cnp)
        insert_query = f"""
            INSERT INTO credit_cards (CNP, card_number, card_type, credit_limit, outstanding_amount, due_date)
            VALUES (
                '{credit_card['cnp']}',
                '{credit_card['card_number']}',
                '{credit_card['card_type']}',
                '{credit_card['credit_limit']}',
                '{credit_card['outstanding_amount']}',
                '{credit_card['due_date']}'
            )
        """
        db_executor(insert_query)


def generate_random_credit_cards_for_users():
    user_cnp_list = get_all_user_cnp()  # You need to implement this function
    for cnp in user_cnp_list:
        for _ in range(random.randint(0, 3)):
            insert_random_credit_card_query(cnp)


def transfer_funds_query(sender_cnp: str, recipient_account_number: str, transfer_amount: float) -> None:
    transfer_query = f"""
        BEGIN;
            UPDATE users SET balance = balance - {transfer_amount} WHERE CNP='{sender_cnp}';
            UPDATE users SET balance = balance + {transfer_amount} WHERE account_number='{recipient_account_number}';
        COMMIT;
    """
    db_executor(transfer_query)


def pay_bills_query(cnp: str, total_sum_of_bills: int) -> None:
    pay_query = f"""
        BEGIN;
            UPDATE users SET balance = balance - {total_sum_of_bills} WHERE CNP='{cnp}';
            UPDATE bills SET gas = 0, electricity = 0, water = 0, rent = 0 WHERE cnp='{cnp}';
        COMMIT;
    """
    db_executor(pay_query)


def pay_gas_bill_query(cnp: str, gas_bill_amount: int) -> None:
    pay_query = f"""
        BEGIN;
            UPDATE users SET balance = balance - {gas_bill_amount} WHERE CNP='{cnp}';
            UPDATE bills SET gas = 0 WHERE cnp='{cnp}';
        COMMIT;
    """
    db_executor(pay_query)


def pay_electricity_bill_query(cnp: str, electricity_bill_amount: int) -> None:
    pay_query = f"""
        BEGIN;
            UPDATE users SET balance = balance - {electricity_bill_amount} WHERE CNP='{cnp}';
            UPDATE bills SET electricity = 0 WHERE cnp='{cnp}';
        COMMIT;
    """
    db_executor(pay_query)


def pay_water_bill_query(cnp: str, water_bill_amount: int) -> None:
    pay_query = f"""
        BEGIN;
            UPDATE users SET balance = balance - {water_bill_amount} WHERE CNP='{cnp}';
            UPDATE bills SET water = 0 WHERE cnp='{cnp}';
        COMMIT;
    """
    db_executor(pay_query)


def pay_rent_bill_query(cnp: str, rent_bill_amount: int) -> None:
    pay_query = f"""
        BEGIN;
            UPDATE users SET balance = balance - {rent_bill_amount} WHERE CNP='{cnp}';
            UPDATE bills SET rent = 0 WHERE cnp='{cnp}';
        COMMIT;
    """
    db_executor(pay_query)


def log_transfer_query(sender_cnp: str, recipient_account_number: str, transfer_amount: float) -> None:
    log_query = f"""
        INSERT INTO transactions (CNP, transaction_type, target, amount)
        VALUES ('{sender_cnp}', 'Transfer', '{recipient_account_number}', {transfer_amount});
    """
    db_executor(log_query)


def log_payment_query(cnp: str, bill_type: str, amount: int) -> None:
    log_query = f"""
        INSERT INTO transactions (CNP, transaction_type, target, amount)
        VALUES ('{cnp}', 'Bill Payment', '{bill_type}', {amount});
    """
    db_executor(log_query)


# Find inside tables #
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


def get_account_number_by_cnp_query(cnp: str) -> str:
    account_number_query = f"SELECT account_number FROM users WHERE CNP='{cnp}'"
    result = db_executor(account_number_query)

    return result[0][0][0]


def get_balance_by_cnp_query(cnp: str) -> int:
    balance_query = f"SELECT balance FROM users WHERE CNP='{cnp}'"
    result = db_executor(balance_query)
    return result[0][0][0]


def get_total_sum_of_bills_query(cnp: str) -> int:
    sum_of_bills_query = f"SELECT gas + electricity + water + rent FROM bills WHERE cnp='{cnp}'"
    result = db_executor(sum_of_bills_query)

    return result[0][0][0]


def get_gas_bill_query(cnp: str) -> int:
    gas_bill_query = f"SELECT gas FROM bills WHERE cnp='{cnp}'"
    result = db_executor(gas_bill_query)

    return result[0][0][0]


def get_electricity_bill_query(cnp: str) -> int:
    electricity_bill_query = f"SELECT electricity FROM bills WHERE cnp='{cnp}'"
    result = db_executor(electricity_bill_query)

    return result[0][0][0]


def get_water_bill_query(cnp: str) -> int:
    water_bill_query = f"SELECT water FROM bills WHERE cnp='{cnp}'"
    result = db_executor(water_bill_query)

    return result[0][0][0]


def get_rent_bill_query(cnp: str) -> int:
    rent_bill_query = f"SELECT rent FROM bills WHERE cnp='{cnp}'"
    result = db_executor(rent_bill_query)

    return result[0][0][0]


def find_transactions_by_cnp_query(cnp: str) -> list:
    query = "SELECT * FROM transactions WHERE CNP = '%s'" % cnp
    row_data, column_names = db_executor(query)

    transactions = []
    if row_data:
        for row in row_data:
            transaction = dict(zip(column_names, row))
            transactions.append(transaction)
    return transactions


def find_transfers_by_cnp_query(cnp: str) -> list:
    query = "SELECT * FROM transactions WHERE CNP = '%s' AND transaction_type = 'Transfer'" % cnp
    row_data, column_names = db_executor(query)

    transfers = []
    if row_data:
        for row in row_data:
            transfer = dict(zip(column_names, row))
            transfers.append(transfer)
    return transfers


def find_bill_payments_by_cnp_query(cnp: str) -> list:
    query = "SELECT * FROM transactions WHERE CNP = '%s' AND transaction_type = 'Bill Payment'" % cnp
    row_data, column_names = db_executor(query)

    bill_payments = []
    if row_data:
        for row in row_data:
            payment = dict(zip(column_names, row))
            bill_payments.append(payment)
    return bill_payments


def find_transactions_by_cnp_and_date_query(cnp: str, date: str) -> list:
    # Make sure to format the date correctly
    formatted_date = datetime.strptime(date, "%Y-%m-%d").date()
    # Creating the query to select all records that match the CNP and have the same date (ignoring time)
    query = f"SELECT * FROM transactions WHERE CNP = '{cnp}' AND DATE(transaction_date) = '{formatted_date}'"

    row_data, column_names = db_executor(query)
    transactions = []
    if row_data:
        for row in row_data:
            transaction = dict(zip(column_names, row))
            transactions.append(transaction)
    return transactions


def find_transfers_by_cnp_and_account_number_query(cnp: str, account_number: str) -> list:
    query = f"SELECT * FROM transactions WHERE CNP = '{cnp}' AND target = '{account_number}'"
    row_data, column_names = db_executor(query)

    transfers = []
    if row_data:
        for row in row_data:
            transfer = dict(zip(column_names, row))
            transfers.append(transfer)
    return transfers


def get_all_user_cnp():
    query = "SELECT CNP FROM users"
    row_data, column_names = db_executor(query)

    cnp_values = []
    if row_data:
        for row in row_data:
            cnp_values.append(row[0])  # 0 because CNP is the first column in the result
    return cnp_values
