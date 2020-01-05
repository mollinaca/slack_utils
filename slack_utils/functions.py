import sys, os
import configparser
import logging
import urllib.request
import json
import time
import datetime
import pathlib # 3.4 >=
from slack_utils.slack_api import Api
"""
core() から渡されたコマンド、およびオプションを解析し、slack_api で定義される Slack API を実行し、結果を取得する
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

def conv_list (args:dict):
    now = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))

    # まず1回実行する
    api = Api ()
    res = api.conv_list (args)

    # 結果をファイル出力する
    output_files = []
    i = 1
    p = pathlib.Path()
    output_file_dir = p.resolve().joinpath('output')
    output_file = str(output_file_dir) + "/conv_list_" + now + "_" + str(i) + ".json"
    output_files.append(output_file)
    with open(output_file, mode='w') as f:
        f.write(json.dumps(res, indent=4))
        
    # next_cursor の有無を確認する
    if res['response_metadata']['next_cursor']:
        args['next_cursor'] = str(res['response_metadata']['next_cursor'])

        while args['next_cursor']:
            # next_cursor が空になるまで実行する
            i += 1
            api = Api ()
            res = api.conv_list (args)
            output_file = str(output_file_dir) + "/conv_list_" + now + "_" + str(i) + ".json"
            output_files.append(output_file)
            with open(output_file, mode='w') as f:
                f.write(json.dumps(res, indent=4))
            args['next_cursor'] = res['response_metadata']['next_cursor']

    print ("output files:")
    [print (output_file) for output_file in output_files]
    exit (0)
