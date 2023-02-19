import mysql.connector

# Connect to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="marius",
    password="1111",
    database="mydatabase"
)

# Create a cursor
mycursor = mydb.cursor()

# Delete all data and tables in the database
mycursor.execute("DROP DATABASE IF EXISTS mydatabase")
mycursor.execute("CREATE DATABASE mydatabase")
mycursor.execute("USE mydatabase")

# Create the users table
mycursor.execute("CREATE TABLE users ("
                 "id INT AUTO_INCREMENT PRIMARY KEY, "
                 "CNP VARCHAR(4), "
                 "password VARCHAR(255), "
                 "account_number VARCHAR(4), "
                 "name VARCHAR(255), "
                 "surname VARCHAR(255), "
                 "age VARCHAR(2), "
                 "register_date DATE, "
                 "balance INT)")

# Commit the changes
mydb.commit()

# Close the cursor and database connection
mycursor.close()
mydb.close()
