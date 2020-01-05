import sys
import logging
from slack_utils.slack_utils import command, usage

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('Started')
    logging.info(str(sys.argv))
    if sys.argv[1:2]:
        sys.exit(command(sys.argv[1:]))
    else:
        usage ()