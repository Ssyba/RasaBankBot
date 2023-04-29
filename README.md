# RasaBankBot
This will be a bot in the RASA framework that will take the place of an online bank teller to help customers.

# Requirements:
- Python 3.8.10 or higher

# Hot to install:
1. Pull code to your local machine.
2. In CLI run: 
   1. python3 -m venv ./venv 
      - this is to create a python virtual environment
   2. .\venv\Scripts\activate
      - this is to activate the previously created virtual environment
   3. pip3 install pip && pip3 install rasa==3.1.1
      - this is to update pip and install rasa locally
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
3. rasa -h
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

# How to create DB:
**This will clear the database, create a table users with:**
-id(int)
-CNP(string 4 chars numbers only), last 2 digits show person age
-identify password(min 6 chars, 1 letter, 1 number, and confirmation)
-account number(string 4 chars number only), 
-name(string, letters only, capitalize before logging in the database), 
-surname(string, letters only, capitalize before logging in the database), 
-age(string 2 number chars), 
-registration date(date format), 
-balance(int), 

- **Steps**:
Right click on database_schema_structure_update.py and click on Run.
Or in the cmd(inside the project folder): python database_schema_structure_update.py

# Available functionalities at this time:
1. Fully built home welcome page for Marius Bank.
2. Greet the user
3. Refresh session, logout on page refresh.
4. Log the user in automatically - for debugging purposes.
5. Answer to: What are you?/Are you a bot?
6. Show company policies, redirects to a webpage with website policies.
7. Create new user.
8. Ask for check cnp again, if you think you mistyped it.
9. Login when app start, or using "log me in" or similar
10. Logout using keywords "log me out" or similar.
11. Break outside any loop using keyword "break" or similar.
12. Show user information for:
    - Show all the user's information(show me my info)
    - Show the user's CNP(show me my cnp)
    - Show the user's name(show me my name)
    - Show the user's surname(show me my surname)
    - Show the user's age(show me my age)
    - Show the user's account number(show me my account number)
    - Show the user's registration date(show me my registration date)
    - Show the user's current balance(show me my balance)
    - Show the user's current slots(show my slots) - this is for debugging purposes
13. Can't use break outside a loop, use is informed there is nothing to break.
14. When the bot does not know what to do there is a standard message is shows to the user.
15. Transfer funds to another account by account number.
16. Show user bills:
    - Show the user's bills and total(show me my bills)
    - Show the user's gas bill(show my gas bill)
    - Show the user's electricity bill(show my electricity bill)
    - Show the user's water bill(show my water bill)
    - Show the user's rent bill(show my rent bill)
17. Is users tries to login but is already login, message will be displayed.
18. Pay bills:
    - Pay my bills(I want to pay my bills)
    - Pay my gas bill(I want to pay my gas bill)
    - Pay my electricity bill(I want to pay my electricity bill)
    - Pay my water bill(I want to pay my water bill)
    - Pay my rent bill(I want to pay my rent bill)
