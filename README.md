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
