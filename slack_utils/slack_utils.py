import sys
import logging
from optparse import OptionParser
from slack_utils.functions import api_test, auth_test, incoming_webhook
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

def command (argv:list):
    global command
    command = argv[0]

    if command == "test":
        print ("test")
        exit (0)

    elif command == "api_test":
        api_test ()

    elif command == "auth_test":
        auth_test ()

    elif command == "incoming_webhook":
        incoming_webhook (argv[1:])
#
#    elif command == "post":
#        if argv[1:2]:
#            post (argv[1:])
#        else:    
#            logging.warning('Usage -> $ slack_utils post ${message}')
#            exit (1)
#
#    elif command == "post_quote":
#        if argv[1:2]:
#            post_quote (argv[1:])
#        else:    
#            logging.warning('Usage -> $ slack_utils post_quote ${message}')
#            exit (1)
#
#
#    elif command == "conv_list":
#        """
#        $ slack_utils conv_list [public|private] [true|false]'
#        default:
#            arg2(type): both of public and private 
#            arg3(exclude_archive): true
#        """
#        conv_list (argv[1:])
#
#    elif command == "post_quote":
#        post (str(argv[1]))
#    elif command == "notice":
#        notice (str(argv[1]))
#    elif command == "warning":
#        warning (str(argv[1]))
#    elif command == "alert":
#        alert (str(argv[1]))

    else:
        usage ()
