import sys
import logging
from slack_utils.slack_utils import command

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('Started')
    logging.info(str(sys.argv))
    sys.exit(command(sys.argv[1:]))
