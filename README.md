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
-register date(date format), 
-balance(int), 

- **Steps**:
Right click on database_schema_structure_update.py and click on Run.
Or in the cmd(inside the project folder): python database_schema_structure_update.py

# Available functionalities at this time:
1. Respond to any type of greet(ex. hello, hi, how are you, howdy, etc.)
2. Able to find user and greet the user by CNP, will show message notifying the user if he's not in the db.