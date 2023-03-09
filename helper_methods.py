import mysql.connector


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
    if query[0] in ["INSERT", "UPDATE", "DELETE", "COMMIT", "ROLLBACK", "SAVEPOINT", "SET TRANSACTION"]:
        # Commit the changes
        cursor.commit()
    else:
        # Fetch the results
        result = cursor.fetchall()

    # Close the cursor and database connection
    cursor.close()
    db_connection.close()

    return result
