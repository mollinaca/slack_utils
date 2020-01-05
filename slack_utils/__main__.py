import sys
import logging
import argparse
from argparse import RawTextHelpFormatter
from slack_utils.slack_utils import core, usage

def main():

    parser = argparse.ArgumentParser(
        prog='slack_utils',
        description=" slack utility tool for Slack Administrator, \n see also https://github.com/mollinaca/slack_utils",
        formatter_class=RawTextHelpFormatter,
        add_help=True
    )
    commands=(" \n"
    " api_test : exec api.test \n"
    " auth_test : exec auth.test \n"
    " incoming_webhook [text] : post text message via incoming webhook \n"
    "\n"
    " post -c [channel_id|channel_name] -t [text] : post text message via chat.Postmessage \n"
    "\t channel_id\t: for example, CXXXXXXXX, or GXXXXXXXX\n"
    "\t channel_name\t: for example, yourchannel\n"
    "\n"
    " conv_list -t [public|private] -e [true|false] : get conversations list via conversations.list \n"
    "\t -t : types, private or public. default: both of public and private \n"
    "\t -e : exclude_archived, default: true\n")
    parser.add_argument("command", choices=['api_test','auth_test','incoming_webhook','post','conv_list'], help=commands)
    args = parser.parse_args()

    print (args)
    command = str(args.command)
    logging.info('command:'+command)
    print (sys.argv)

#    if args.verbosity:
#        print("verbosity turned on")

    logging.basicConfig(level=logging.INFO)
    logging.info('Started')
    logging.info(str(sys.argv))

    if sys.argv[1:2]:
        sys.exit(core(command, sys.argv[2:]))
