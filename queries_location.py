from helper_methods import db_executor


def create_users_table():
    return db_executor(
        "CREATE TABLE users ("
        "id INT AUTO_INCREMENT PRIMARY KEY, "
        "CNP VARCHAR(4), "
        "password VARCHAR(255), "
        "account_number VARCHAR(4), "
        "name VARCHAR(255), "
        "surname VARCHAR(255), "
        "age VARCHAR(2), "
        "register_date DATE, "
        "balance INT)"
    )


def delete_users_table():
    return db_executor("DROP TABLE users")


def find_user_by_cnp_query(cnp: str) -> str:
    return db_executor("SELECT * FROM users WHERE CNP = '%s'" % cnp)


def find_user_name_by_cnp_query(cnp: str) -> str:
    return db_executor("SELECT name FROM users WHERE cnp = '%s'" % cnp)
