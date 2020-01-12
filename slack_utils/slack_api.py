import sys, os
import configparser
import logging
import urllib.request
import json
import time
"""
SlackAPI を使ったHTTPリクエストとその結果の取得し、レスポンスボディとして return する
urllibによるHTTPリクエストでエラーがあった場合は、
以下の順番でエラー処理する
* HTTP通信自体の失敗 → 11秒まってリトライし、それでもダメなら stdout にエラーを出力  
* HTTP通信が 4xx,5xx だった場合 → 61 秒まってリトライし、それでもダメなら stdout にエラーを出力して終了
  * Slack API による rate limit (HTTP429) だった場合を含む
     About Rate Limit: https://api.slack.com/docs/rate-limits
* Slack API による結果取得のレスポンスボディにおいて、 "ok": false だった場合 → 61 秒まってリトライし、それでもダメなら stdout にエラーを出力して終了
"""

## API実行用クラス
class Exec_api:

#    def __init__(self):
#        return 0
#
#    def __del__(self):
#        return 0

    def conf (self):
        """
        load config.ini to global variables
        """
        global token, default_channel, webhook_url, api_url

        cfg = configparser.ConfigParser()
        cfg.read(os.path.dirname(__file__)+"/config.ini")
        token = cfg["slack"]["token"]
        default_channel = cfg["slack"]["channel"]
        webhook_url = cfg["slack"]["webhook_url"]
        api_url = "https://slack.com/api/"
        
        logging.info('conf() loaded')
        return 0

    def exec (self, req):
        """
        explanation:
            exec Slack API
        
        Args:
            req: urllib request object
        
        Return:
            body: Json object (dict)
        
        正常に完了した場合は レスポンスボディ を返す
        失敗した場合は、以下の内容 json を返す
        {"ok": false}
        """
        body = json.loads(b'{"ok": false}'.decode('utf-8'))

        try:
            with urllib.request.urlopen(req) as res:
                body = json.loads(res.read().decode('utf-8'))
                logging.info ("responsebody:")
        except urllib.error.HTTPError as err:
            logging.warn ("catch HTTPError:" + str(err.code))
            logging.info ("retry once")
            time.sleep(61)
    
            try:
                with urllib.request.urlopen(req) as res:
                    body = json.loads(res.read().decode('utf-8'))
                    logging.info ("responsebody:")
            except urllib.error.HTTPError as err:
                logging.warn ("catch HTTPError:" + str(err.code))
                logging.info ("err, end")
    
        except urllib.error.URLError as err:
            logging.warn ("catch URLError:" + str(err.reason))
            logging.info ("retry once")
            time.sleep(11)
    
            try:
                with urllib.request.urlopen(req) as res:
                    body = json.loads(res.read().decode('utf-8'))
                    logging.info ("responsebody:")
            except urllib.error.URLError as err:
                    logging.warn ("catch URLError:" + str(err.reason))
                    logging.info ("err, end")

        return body


class Api():

    def api_test (self):
        """
        https://api.slack.com/methods/api.test
        """
        res = Exec_api ()
        url = "https://slack.com/api/api.test"

        req = urllib.request.Request(url)
        res = Exec_api ()
        body = res.exec (req)
        return body

    def auth_test (self):
        """
        https://api.slack.com/methods/auth.test
        """
        res = Exec_api ()
        url = "https://slack.com/api/auth.test"
        res.conf ()
        params = {
            'token': token,
        }

        req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)))
        body = res.exec (req)
        return body

    def incoming_webhook (self, message:str):
        """
        use incoimng-webhook
        incoming-webhook は結果をjsonで返さないので、これだけ特殊処理
        """
        res = Exec_api ()
        res.conf ()
        data = {
            "text": message
        }
        headers = {
            "Content-Type": "application/json",
        }
        url = webhook_url

        req = urllib.request.Request(url, json.dumps(data).encode(), headers)
        with urllib.request.urlopen(req) as res:
            body = res.read().decode('utf-8')
            logging.info ("responsebody:"+body)
            if body == "ok":
                body = json.loads('{"ok": true}')
        return body

    def post (self, args:list):
        """
        https://api.slack.com/methods/chat.postMessage
        """
        res = Exec_api ()
        res.conf ()
        url = "https://slack.com/api/chat.postMessage"
        method = "POST"
        message = str(args['message'])

        if 'channel' in args:
            channel = str(args['channel'])
        else:
            channel = default_channel

        headers = {
            "Content-Type": "application/json",
        }

        params = {
            'token': token,
            'channel': channel,
            'text': message
        }
        if 'thread' in args:
            params['thread_ts'] = args['thread']

        req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)), method=method, headers=headers)
        body = res.exec (req)
        return body

    def conv_list (self, args:dict):
        """
        https://api.slack.com/methods/conversations.list
        arg:
            types
            exclude_arvhiced
            next_cursor
        default:
            types: "public, private"
            exclude_archived: "true"
            next_cursor: null
        """
        res = Exec_api ()
        res.conf ()
        method = "GET"
        url = "https://slack.com/api/conversations.list"
        params = {
            'token': token,
            'types': args['types'],
            'exclude_archived': args['exclude_archived'],
            'limit': 1000
        }
        if args['next_cursor']:
            params['cursor'] = args['next_cursor']

        req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)), method=method)
        body = res.exec (req)

        return body

    def conv_info (self, args:dict):
        """
        https://api.slack.com/methods/conversations.info
        arg:
            channel:
        default:
            channel: set in config.ini
        """
        res = Exec_api ()
        res.conf ()
        method = "GET"
        url = "https://slack.com/api/conversations.info"
        if not args['channel']:
            args['channel']=default_channel

        params = {
            'token': token,
            'channel': args['channel']
        }

        print (params)
        req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)), method=method)
        body = res.exec (req)

        return body


    def users_list (self, args:dict):
        """
        https://api.slack.com/methods/users.list
        arg:
            next_cursor
        default:
            next_cursor: null
        """
        res = Exec_api ()
        res.conf ()
        method = "GET"
        url = "https://slack.com/api/users.list"
        params = {
            'token': token,
            'limit': 1000
        }
        if args['next_cursor']:
            params['cursor'] = args['next_cursor']

        req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)), method=method)
        body = res.exec (req)

        return body
