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

def incoming_webhook (args:dict):
    message = str(args['message'])
    api = Api ()
    res = api.incoming_webhook (message)
    print (json.dumps(res, indent=4))
    exit (0)

def post (args:dict):
    api = Api ()
    res = api.post (args)
    print (json.dumps(res, indent=4))
    exit (0)

def conv_list (argv:list):
    if argv[0:1]:
        if argv[0] == "public":
            argv.insert (0, "public_channel")
        elif argv[0] == "private":
            argv.insert (0, "private_channel")
        else:
            argv.insert (0, "public_channel,private_channel")
    else:
        argv.insert (0, "public_channel,private_channel")

    if argv[1:2]:
        if not argv[1] == "true" or not argv[1] == "true" :
            argv.insert(1, "true")
    else:
        argv.insert(1, "true")

    next_cursor = "default"
    argv.insert (2, next_cursor)
    while not next_cursor:
        api = Api ()
        res = api.conv_list (argv)
        print (json.dumps(res, indent=4))

    exit (0)

