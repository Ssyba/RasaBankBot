def find_user_by_cnp_query(cnp: str) -> str:
    return "SELECT * FROM users WHERE CNP = '%s'" % cnp


def find_user_name_by_cnp_query(cnp: str) -> str:
    return "SELECT name FROM users WHERE cnp = '%s'" % cnp

