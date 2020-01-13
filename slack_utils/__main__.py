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
    commands = ['test', 'api_test', 'auth_test', 'incoming_webhook', 'post', 'post_quote', 'conv_list', 'conv_id_list', 'conv_info', 'conv_history', 'users_list', 'users_info']
    command_help = (" \n"
    " api_test : exec api.test \n"
    " auth_test : exec auth.test \n"
    " incoming_webhook [text] : post text message via incoming webhook \n"
    "\n"
    " post -c [channel_id|channel_name] -m [text] --thread [thread] : post text message via chat.Postmessage \n"
    "\t channel_id\t: for example, CXXXXXXXX, or GXXXXXXXX\n"
    "\t channel_name\t: for example, yourchannel\n"
    " post_quote -c [channel_id|channel_name] -m [text] : post text message via chat.Postmessage. Automaticaly add blockquote(```) to message \n"
    "\t --thread\t: if you want to post to thread, input this param (option)"
    "\t -c:\n"
    "\t\t channel_id\t: for example, CXXXXXXXX, or GXXXXXXXX\n"
    "\t\t channel_name\t: for example, yourchannel\n"
    "\n"
    " conv_list -t [public|private] -e [true|false] : get conversations list raw json via conversations.list \n"
    " conv_id_list -t [public|private] -e [true|false] : get conversations list only channel id .txt via conversations.list \n"
    "\t -t : types, private or public. default: both of public and private \n"
    "\t -e : exclude_archived, default: true\n")
    " conv_history -c [channel_id|channel_name] : get conversations history via conversations.history \n"
    " conv_info -c [channel_id|channel_name] : get conversations info via conversations.info \n"
    " users_list : get users list via users.list \n"
    " users_info -u [user_id]: get users info via users.info \n"
    "\t -u : user_id"


    parser.add_argument('command', choices=commands, help=command_help)
    parser.add_argument('-c', '--channel', help='channel_id or channel_name (default set in config.ini)')
    parser.add_argument('-m', '--message', help='simple string message to post (default "no message")', default='no message')
    parser.add_argument('-u', '--user', help='channel_id or channel_name (default set in config.ini)')
    parser.add_argument('-t', '--types', help='type of target channels (default both of public and private)', default='public_channel, private_channel')
    parser.add_argument('-e', '--exclude_archived', help='exclude_archived(default true)', default='true')
    parser.add_argument('--thread', help='thread to post')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    logging.info('Started')
    logging.info(str(sys.argv))

    sys.exit(core(args))
