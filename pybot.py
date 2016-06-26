"""
Based on guide posted at:
https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
"""

# force decimal divison by default
from __future__ import division

import os
import sys
import time

try:
    from slackclient import SlackClient
except ImportError as err:
    print(err)
    print("\nDid you forget to `$ pip install slackclient`? Quitting.")
    sys.exit(1)

# Assign the token via environment variable (Heroku `config vars`)
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
VIDCARD_COMMAND = "vidcard"
HELP_COMMAND = "help"
ABOUT_COMMAND = "aboutyou"

slack_client = SlackClient(SLACK_BOT_TOKEN)


def vidcard_calc(dollar_amount):
    one_vidcard_value = 300
    num_vid_cards = dollar_amount / one_vidcard_value
    return num_vid_cards

def help_menu(help_term=None):
    """
    :param help_term: A dictionary of commands and their explanation. Defaults to None if help_menu called without arguments
    :return: output
    """

    # Dictionary of help items. Keys are the command, value is the explanation
    help_items = {
        "aboutyou": "Type `@pybot: aboutyou` --> returns information about me.",
        "vidcard": "Type `@pybot: vidcard {dollar amount here}` --> returns the number of video cards you could buy for that dollar amount."
    }

    output = ""

    # just get the explanation for one command
    if help_term in help_items:
        output += "Here is help on that command:\n"
        output = help_items[help_term]

    # if user doesn't pass a specific term list all the help
    elif help_term == None:
        output += "Here is help for all my commands:\n"
        for i in help_items.values():
            output += "{0}\n".format(i)
    return output


def handle_command(command, channel):
    """
    Receives commands directed at bot & determines if valid.

    :param command:
    :param channel:
    :return:
    """
    response = """
        I don't understand that command. If this is an issue / error, please track it.
        https://github.com/cupway/pybot-cupway/issues
        For help, type `@pybot: help`
    """

    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure .. write some code and I can do that."


    # Define the @pybot: help command
    if command.startswith(HELP_COMMAND):
        # break the command sent to @pybot into a list
        help_string_list = command.split(" ")
        # user called just @pybot: help
        if len(help_string_list) == 1:
            response = help_menu()
        # user called @pybot: help {command}
        if len(help_string_list) == 2:
            response = help_menu(help_string_list[1])


    # Define the @pybot: aboutyou command
    if command.startswith(ABOUT_COMMAND):
        response = """
        I'm a Python bot. My code is here: https://github.com/cupway/pybot-cupway\n
        I'm hosted on Heroku. Contributions, pull requests and feature requests welcome.\n
        Contact @scottae or @ericdorsey for additional details.
        """

    if command.startswith(VIDCARD_COMMAND):
        print(command) # only shows up in logging, $ heroku log -n 50
        command_dollar_amount = command.split(" ")[1]
        # Get rid of preceding dollar signs if present
        if command_dollar_amount.startswith("$"):
            command_dollar_amount = command_dollar_amount.lstrip("$")
        # Get rid of commas if present
        if "," in command_dollar_amount:
            command_dollar_amount = command_dollar_amount.replace(",", "")
        try:
            command_dollar_amount = int(command_dollar_amount)
            vidcard_number = vidcard_calc(command_dollar_amount)
            # if it's an even number, example 20.0, strip off the decimal
            if vidcard_number % 2 == 0:
                vidcard_number = int(vidcard_number)
            # if it's not an even float, limit decimals to 2 places
            if (vidcard_number % 2 == 0) == False:
                vidcard_number = round(vidcard_number, 2)
            if vidcard_number < 1:
                response = "That's not even one video card ;("
            if vidcard_number >= 1:
                vidcard_number = "{:,}".format(vidcard_number)
                response = "That's {0} video cards!".format(vidcard_number)
        except ValueError:
            response = "You need to give me a number!"


    # Always send the response we built above:
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True, unfurl_links=False, unfurl_media=True)


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