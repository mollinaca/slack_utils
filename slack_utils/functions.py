import sys, os
import configparser
import logging
import urllib.request
import json
import time
from slack_utils.slack_api import Api
"""
slack_api で定義される Slack API を実行し、結果を取得する
取得した結果を機能ごとに処理し、以下のいずれか、または組み合わせで出力する
* stdout
* slack へメッセージをPOST
* ファイル出力
  * .json
  * .csv
* ファイルをSlackへ upload
  * 単体メッセージとして upload
  * まずメッセージをPOSTして、そのスレッドにファイルを upload
"""

def api_test ():
    api = Api ()
    res = api.api_test ()
    print (json.dumps(res, indent=4))
    exit (0)

def auth_test ():
    api = Api ()
    res = api.auth_test ()
    print (json.dumps(res, indent=4))
    exit (0)

def incoming_webhook (argv:list):
    if not argv[0:1]:
        logging.warning('Usage -> $ slack_utils incoming_webhook ${message}')
        exit (1)
    api = Api ()
    res = api.incoming_webhook (argv)
    print (json.dumps(res, indent=4))
    exit (0)
