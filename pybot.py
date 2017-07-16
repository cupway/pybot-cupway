# Force decimal divison by default
from __future__ import division

import os
import sys
import time
import requests
import signal
import re

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
    print("\nIs SLACK_BOT_TOKEN configured in Heroku app Settings w/ a valid Slack token?")

# Use the BOT_ID gathered from get_pybot_id.py
BOT_ID = "U1J60L0F2"

#AT_BOT = "<@" + BOT_ID + ">:"

# All possible commands
all_commands = {
        "VIDCARD_COMMAND" : "vidcard",
        "HELP_COMMAND" : "help",
        "ABOUT_COMMAND" : "aboutyou",
        "GAME_OF_THRONES" : ["gotme", "got me"],
        "KING_IN_THE_NORTH" : "king",
        "CHANNEL_INFO" : "chaninfo",
        "GIBBERISH" : ["gibberish", "nonsense"]
}

slack_client = SlackClient(SLACK_BOT_TOKEN)

def get_id_from_room_name():
    channel_info = slack_client.api_call("channels.list", exclude_archived=True)
    return channel_info

def signal_term_handler(signal, frame):
    """
    Monitors for a SIGTERM; Heroku restarts Dynos approx once every 24 hrs
    :param signal: signal number - usually 15 for SIGTERM
    :param frame: current stack frame
    :return: N/A
    """
    if signal == 15:
        print("*** SIGTERM received. Exiting gracefully ..")
        # SIGTERM signals are normal / expected when Heroku Dyno restarts
        sys.exit(0)
    else:
        # signal other than SIGTERM received
        print("*** signal received: {0}").format(signal)

# Monitor for SIGTERM signal
signal.signal(signal.SIGTERM, signal_term_handler)


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
        "aboutyou": "Type `@pybot aboutyou` --> returns information about @pybot",
        "vidcard": "Type `@pybot vidcard {dollar amount}` --> returns the number of video cards you could buy for that dollar amount.",
        "gotme": "Type `@pybot gotme` (alt: `got me`) --> returns a Game of Thrones quote from `https://got-quotes.herokuapp.com/quotes` API",
        "king": "Type `@pybot king` --> returns useful information about the King in the North",
        "chaninfo": "Type `@pybot chaninfo` --> returns channel information",
        "gibberish": "Type `@pybot gibberish` (alt: `nonsense`) --> returns gibberish",
        "help" : "Type `@pybot help` --> returns help information"
    }

    output = ""

    # just get the explanation for one command
    if help_term != None and help_term in help_items:
        help_term = help_term.strip()
        output = help_items[help_term]

    # if user doesn't pass a specific term list all the help
    elif help_term == None:
        for i in sorted(help_items.values()):
            output += "{0}\n".format(i)
    return output


def handle_command(command, channel, all_commands):
    """
    Receives commands directed at bot & determines if valid.

    :param command: command passed by user
    :param channel:
    :return: N/A
    """

    # Default response
    if command not in all_commands.values(): 
        response = "I don't understand that command. If this is an issue / error, please track it:\
        \nhttps://github.com/cupway/pybot-cupway/issues\
        \nFor help, type `@pybot help`"

    # Define the @pybot: chaninfo comamnd
    if command.startswith(all_commands["CHANNEL_INFO"]):
        response = get_id_from_room_name()

    # Define the @pybot: gibberish command
    for i in all_commands["GIBBERISH"]:
        if i in command:
            r = requests.get("http://www.randomtext.me/api/gibberish/p-1/5-12")
            if r.status_code == 200:
                r = r.json()
                response = re.sub("<.*?>", "", r["text_out"]).rstrip()
            else:
                response = "GET request to `http://www.randomtext.me/api/gibberish/p-1/5-12` not `200 OK`\
                \nGET status code was: {0}".format(r.status_code)

    # Define the @pybot: gotme command
    for i in all_commands["GAME_OF_THRONES"]:
        if i in command:
            r = requests.get("https://got-quotes.herokuapp.com/quotes")
            if r.status_code == 200:
                r = r.json()
                r["quote"] = r["quote"].encode("ascii", "ignore")
                r["character"] = r["character"].encode("ascii", "ignore")
                try:
                    response = "{0} -{1}".format(r["quote"], r["character"])
                except UnicodeError as uni_error:
                    response = "Oh no! I had a Unicode error: {0}".format(uni_error)
            else:
                response = "GET request to `https://got-quotes.herokuapp.com/quotes` not `200 OK`\
                \nGET status code was: {0}".format(r.status_code)

    # Define the @pybot: help command
    if command.startswith(all_commands["HELP_COMMAND"]):
        """
        # break the command sent to @pybot into a list
        help_string_list = command.split(" ")
        # user called just @pybot: help
        if len(help_string_list) == 1:
            response = help_menu()
        # user called @pybot: help {command}
        if len(help_string_list) == 2:
            response = help_menu(help_string_list[1])
        # user passes more than one term, default to plain @pybot: help
        if len(help_string_list) > 2:
        """
        response = help_menu()

    # Define the @pybot: aboutyou command
    if command.startswith(all_commands["ABOUT_COMMAND"]):
        response = "I'm a Python bot. My code is here: https://github.com/cupway/pybot-cupway\
        \nI'm hosted on Heroku. Contributions, pull requests and feature requests welcome."

    # Define @pybot: king command
    if command.startswith(all_commands["KING_IN_THE_NORTH"]):
        response = "*DAKINGINDANORF!!* :rpluslequalsj: *DAKINGINDANORFF!!*"

    # Define @pybot: vidcard command
    if command.startswith(all_commands["VIDCARD_COMMAND"]):
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

def parse_command(command, dm_message):
    """
    Determines wether to pass a command to handle_command()
    Public commands without @pybot return None instead of getting passed along

    :param command:
    :param pub_or_dm:
    :return:
    """
    
    print("\n")
    print("*" * 15)
    print("command variable in parse_command: {0}".format(command))
    print("dm_message variable status in parse_command: {0}".format(dm_message))
    print("@pybot in command?: {0}".format("@pybot" in command))
    print("<@U1J60L0F2> in command?: {0}".format("<@U1J60L0F2>" in command))
    print("*" * 15)
    

    if dm_message == True:
        print("dm_message is True block hit!")
        if command.startswith("<@U1J60L0F2>"):
            command = command.lstrip("<@U1J60L0F2> ")
        print("new command is {0}: ".format(command))
        return command

    # public chat room message and @pybot in message
    elif dm_message == False and "<@U1J60L0F2>" in command == True:
    #elif dm_message == False:
        print("public message and @pybot found block hit!")
        command = command.lstrip("<@U1J60L0F2> ")
        print("new command is {0}: ".format(command))
        return command

    else:
        print("*" * 15)
        print("Else block hit -- this shouldn't happen")
        print("*" * 15)
        
if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print("Pybot connected and running (AKA; its working)")
        while True:
            event_list = slack_client.rtm_read()
            if len(event_list) > 0:
                for event in event_list:
                    # we only care about "message" type events
                    print("\nEvent was:\n{0}".format(event))
                    if event["type"] == "message":
                        # set to True only if message doesn't come from a bot
                        bot_id_in_event = "bot_id" in event
                        command = event["text"]
                        channel = event["channel"]
                        #print("channel is {0}".format(channel))
                        # public chat or direct message with bot?
                        dm_message = False
                        if channel.startswith("D"):
                            dm_message = True
                        #if command and (bot_id_in_event == True):
                        command = parse_command(command, dm_message)
                        # Only respond if the bot didn't issue the prior event text
                        # Need to check against actual bot_id if more bots added
                        if command and channel and (bot_id_in_event == False):
                            print("command before handle_command() call: {0}".format(command))
                            handle_command(command, channel, all_commands)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
