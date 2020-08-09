# beachballbot
Question Chat Bot for bonding during Honors orientation 2020. Replaces the normal beach ball with questions due to COVID concerns.

## Structure
questions-core is meant to be a backend for many different types of chat bots.

## Usage
Run app.py as a flask app to start the REST api and groupme bot.
- The GroupMe bot must have a config file defined giving it a name and mapping from group_id to bot_id for that chat.

- To run as a Flask app, you need the libraries specified in requirements.txt.
Run the following commands from the project root.
   
   On windows to install the dependencies:
   - $ py -m pip install -r requirements.txt
   
   Then to run:
   - $ py -m flask run 

Run discord.py as a normal python script to start it.
- It must be configured with your own bot API token in conf/discord_token.txt
