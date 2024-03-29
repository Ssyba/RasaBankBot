# RasaBankBot
This is a bot in the RASA framework that will take the place of an online bank teller to help customers.
The interface is a small widget at the bottom of the bank page where the user can chat with the bot and even perform 
bank transactions of various kinds or get information about the bank or his own finances or other relevant information.

# Requirements:
- Python 3.8.10 or higher
- Rasa 3.4.4
- rasa-webchat 1.0.1
- mysqlclient 2.1.1

# Hot to install:
1. Pull code to your local machine.
2. In CLI run: 
   1. python3 -m venv ./venv 
      - this is to create a python virtual environment
   2. .\venv\Scripts\activate
      - this is to activate the previously created virtual environment
   3. pip3 install pip
      - this is to update pip
   4. pip install -r requirements.txt
      - this will install all the required packages the project needs

# Commands for CLI:
1. rasa train
   - this will train all the stories
   - rasa train nlu
     - to only train NLU models
   - rasa train core
     - to only train Core models
2. rasa shell
   - to start the bot
3. rasa data validate
   - to check if there are any rasa framework issues
4. rasa test nlu
   - to get a more details report of nlu, intent incompatibility and clashes
5. rasa -h
   - to see all available commands

# Tutorial for using the web interface snippet:
1. Download https://github.com/botfront/rasa-webchat
2. Unpack it and go inside the folder of the downloaded project
3. Copy the path and open it inside a CLI
4. Run: npm install rasa-webchat
5. Start your action server.
6. Start the bot using: rasa run -m models --enable-api --cors "*" --debug
7. From the RasaBankBot project folder open up index.html in a browser.

# Run/Debug Configurations:
![rasa shell](https://user-images.githubusercontent.com/20334644/217662204-fb40ff9d-8f4d-4ce0-8eb7-0d07d31db02f.PNG)
To start the action server, this will work for breakpoints in intellij or pycharm, use the script provided in the picture below and tart it like this:
![rasa action server](https://user-images.githubusercontent.com/20334644/219470306-a998c38d-5b2a-4598-8d2e-5a39ae35f4d3.PNG)

- **Steps**:
Right click on database_schema_structure_update.py and click on Run.
Or in the cmd(inside the project folder): python database_scripts.py

# Available functionalities at this time:
1. Fully built home welcome page for Marius Bank.
2. Greet the user on application start.
3. Refresh session(5 minutes), logout and refresh session on page refresh.
4. Log the user in automatically - for debugging purposes.
5. Answer to: What are you?/Are you a bot?
6. If the users asks he is redirected to company policies, redirects to a webpage with website policies.
7. User can create a new user from scratch.
8. User can ask for check cnp again, if you think you mistyped it.
9. Login when app starts, or using "log me in" or similar wording.
10. If users tries to login but is already login, message will be displayed.
11. Logout using keywords "log me out" or similar wording.
12. Break outside any loop using keyword "break" or similar wording.
13. Show user information for:
    - Show all the user's information(show me my info)
    - Show the user's CNP(show me my cnp)
    - Show the user's name(show me my name)
    - Show the user's surname(show me my surname)
    - Show the user's age(show me my age)
    - Show the user's account number(show me my account number)
    - Show the user's registration date(show me my registration date)
    - Show the user's current balance(show me my balance)
    - Show the user's current slots(show my slots) - this is for debugging purposes
14. Can't use break outside a loop, user is informed there is nothing to break.
15. When the bot does not know what to do or does not understand, there is a standard fallback message shown to the 
    user.
16. Transfer funds to another account by account number.
17. Show user bills:
    - Show the user's bills and total(show me my bills)
    - Show the user's gas bill(show my gas bill)
    - Show the user's electricity bill(show my electricity bill)
    - Show the user's water bill(show my water bill)
    - Show the user's rent bill(show my rent bill)
18. Pay bills:
    - Pay my bills(I want to pay my bills)
    - Pay my gas bill(I want to pay my gas bill)
    - Pay my electricity bill(I want to pay my electricity bill)
    - Pay my water bill(I want to pay my water bill)
    - Pay my rent bill(I want to pay my rent bill)
19. All the users transactions are logged to the transactions table.
20. User can query transactions by date, type or account number(only for transfers).
21. Credit cards table is created with prepopulated data that attributes random credit cards to each user.
22. User can query to see all credit cards or individual ones by credit card number.
23. The user can also leave feedback that is stored in a feedback table.
24. A script to create, delete, update, clear and populate with realistic looking data is also available.

# Tables used:
1. Users table:
Columns: id, CNP, name, surname, age, password, account_number, registration_date, balance
Purpose: Stores information about bank users, including their personal details and account information.
Bills Table:

2. Bills table:
Columns: id, cnp, gas, electricity, water, rent
Purpose: Stores bill information for each user, including gas, electricity, water, and rent bills.
Transactions Table:

3. Transactions table:
Columns: id, CNP, transaction_type, target, amount, transaction_date
Purpose: Stores transaction details, such as the type of transaction, target account, amount, and transaction date.
Credit Cards Table:

4. Credit cards table: 
Columns: id, CNP, card_number, card_type, credit_limit, outstanding_amount, due_date
Purpose: Stores information about credit cards linked to user accounts, including card details, credit limits, and outstanding amounts.
Feedback Table:

5. Feedback table: 
Columns: id, CNP, feedback, date
Purpose: Stores user feedback and associated dates for future reference.

# Database management script functionalities:
# Users table:
1 - create the users table <br />
2 - delete the users table <br />
3 - clear data from users table <br />
4 - add random users to the user table by cnp (uses the CNP global variable) <br />
5 - delete a user by cnp (uses the CNP global variable) <br />

# Bills table:
6 - create bills table <br />
7 - delete bills table <br />
8 - clear data from bills table <br />
9 - add random taxes for user by cnp (uses the CNP global variable) <br />

# Transactions table:
10 - create transactions table <br />
11 - delete transactions table <br />
12 - clear data from the transactions table <br />

# Credit cards table
13 - create credit cards table <br />
14 - delete credit cards table <br />
15 - clear credit cards table <br />
16 - add random credit card by user cnp (uses the CNP global variable) <br />

# Feedback table
17 - create feedback table <br />
18 - delete feedback table <br />
19 - clear feedback table <br />

# Populate tables
20 - populate users table (uses the NUMBER_OF_USERS global variable) <br />
21 - populate bills table <br />
22 - populate transactions table <br />
23 - populate credit cards table <br />
24 - populate feedback table <br />
