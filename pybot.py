"""
Based on guide posted at:
https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
"""

import os
import sys
import time
try:
    from slackclient import SlackClient
except ImportError as err:
    print("")
    print(err)
    print("")
    print("Did you forget to `$ pip install slackclient`? Quitting.")
    print("")
    sys.exit(1)

# Assign the token via environment variable
try:
    SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
except KeyError:
    print("")
    print("Is SLACK_BOT_TOKEN configured in Heroku app Settings w/ a valid Slack token?")
    print("")

# Use the BOT_ID gathered from get_pybot_id.py
BOT_ID = "U1J60L0F2"

AT_BOT = "<@" + BOT_ID + ">:"
EXAMPLE_COMMAND = "do"

slack_client = SlackClient(SLACK_BOT_TOKEN)

def handle_command(command, channel):
    """
    Receives commands directed at bot & determines if valid.

    :param command:
    :param channel:
    :return:
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
        "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure .. write some code and I can do that."
    if command.startswith("leave"):
        response = "Channel is {0}. Your command was: {1}".format(channel, command)
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
    Returns None unless message directed at bot.

    :param slack_rtm_output:
    :return:
    """
    output_list = slack_rtm_output

    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and "text" in output and AT_BOT in output["text"]:
                # return text after @ mention, whitespace removed
                return output["text"].split(AT_BOT)[1].strip().lower(), \
                    output["channel"]
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print("Pybot connected and running")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")