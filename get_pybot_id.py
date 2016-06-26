# We only ever need to run this once to get the Pybot user ID


import os
import sys
from slackclient import SlackClient


# Assign the token via env variable: $ export SLACK_BOT_TOKEN="token here"
try:
    SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
except KeyError as err:
    print(err)
    print("\nIs SLACK_BOT_TOKEN set in your shell session w/ a valid Slack token?\n")
    print("\nQuitting.")
    sys.exit(1)


BOT_NAME = "pybot"
slack_client = SlackClient(SLACK_BOT_TOKEN)

# if interpreter running module as main program
if __name__ == "__main__":
    # https://api.slack.com/methods/users.list
    api_call = slack_client.api_call("users.list")
    if api_call.get("ok"):
        # get all users to find our bot
        users = api_call.get("members")
        for user in users:
            if "name" in user and user.get("name") == BOT_NAME:
                print("Bot ID for " + user["name"] + " is " + user.get("id"))
    elif "error" in api_call:
        print("\nThere was an error in the API call: {0}\n".format(api_call["error"]))
    else:
        print("\nCould not find bot user with the name " + BOT_NAME)
