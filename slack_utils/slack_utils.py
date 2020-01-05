import sys
import logging
from slack_utils.functions import api_test, auth_test, incoming_webhook, post, conv_list
"""
実行例:
  $ slack_utils api_test
  $ slack_utils incoming_webhook "${message}"
  $ slack_utils post "${message}"
  $ slack_utils conv_list
  $ slack_utils conv_list public
  $ slack_utils conv_list private
"""

def usage ():
    """
    output usage
    """
    message = ("Usage: Todo")
    print (message)
    exit (1)


def core (args):

    if str(args.command):
        command = str(args.command)

    if command == "test":
        print ("test")
        exit (0)

    elif command == "api_test":
        api_test ()

    elif command == "auth_test":
        auth_test ()

    elif command == "incoming_webhook":
        args_d = {
            'message' : args.message
        }
        incoming_webhook (args_d)

    elif command == "post":
        args_d = {
            'message' : str(args.message)
        }
        if not str(args.channel) == "None":
            args_d['channel'] = str(args.channel)
        post (args_d)

    elif command == "post_quote":
        args_d = {
            'message' : '```' + str(args.message) + '```'
        }
        if not str(args.channel) == "None":
            args_d['channel'] = str(args.channel)
        post (args_d)

    elif command == "conv_list":
        args_d = {
            'types' : args.types,
            'exclude_archived' : args.exclude_archived,
            'next_cursor': ""
        }
        conv_list (args_d)

    else:
        usage ()
