# We only ever need to run this once to get the Pybot user ID

try:
    from token import token
    #print(token.SLACK_BOT_TOKEN)
    SLACK_BOT_TOKEN = token.SLACK_BOT_TOKEN
except ImportError:
    print("Couldn't assign SLACK_BOT_TOKEN variable. Likely import issues.")

import os
from slackclient import SlackClient

BOT_NAME = "pybot"
slack_client = SlackClient(SLACK_BOT_TOKEN)

# if interpreter running module as main program
if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if api_call.get("ok"):
        # get all users to find our bot
        users = api_call.get("members")
        for user in users:
            if "name" in user and user.get("name") == BOT_NAME:
                print("Bot ID for " + user["name"] + " is " + user.get("id"))
    else:
        print("Could not find bot user with the name " + BOT_NAME)
