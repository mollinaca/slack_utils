import sys, os
import configparser
import logging
import urllib.request
import json
import time
"""
SlackAPI を使ったHTTPリクエストとその結果の取得、処理を行い
途中経過を logging を使って stderr に出力する
最終結果を stdout と、 Slackチャンネルへ出力する

urllibによるHTTPリクエストでエラーがあった場合は、
以下の順番でエラー処理する
* HTTP通信自体の失敗 → 11秒まってリトライし、それでもダメなら stdout にエラーを出力  
* HTTP通信が 4xx,5xx だった場合 → 61 秒まってリトライし、それでもダメなら stdout にエラーを出力して終了
  * Slack API による rate limit (HTTP429) だった場合を含む
     About Rate Limit: https://api.slack.com/docs/rate-limits
* Slack API による結果取得のレスポンスボディにおいて、 "ok": false だった場合 → 61 秒まってリトライし、それでもダメなら stdout にエラーを出力して終了
"""

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
        global token, channel, webhook_url, api_url

        cfg = configparser.ConfigParser()
        cfg.read(os.path.dirname(__file__)+"/config.ini")
        token = cfg["slack"]["token"]
        channel = cfg["slack"]["channel"]
        webhook_url = cfg["slack"]["webhook_url"]
        api_url = "https://slack.com/api/"
        
        logging.info('conf() loaded')
        return 0

    def exec (self, req):
        """
        slack API を実行する
        正常に完了した場合は レスポンスボディ を返す
        失敗した場合は、以下の json を返す
        { "ok": false}
        """
        body = json.loads(b'{"ok": false}')

        try:
            with urllib.request.urlopen(req) as res:
                body = json.loads(res.read().decode('utf-8'))
                logging.info ("responsebody:")
        except urllib.error.HTTPError as err:
            logging.warn ("catch HTTPError:" + str(err.code))
            logging.info ("retry once")
            time.sleep(11) #61に直す
    
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

def api_test ():
    """
    https://api.slack.com/methods/api.test
    """
    res = Exec_api ()
    url = "https://slack.com/api/api.test"
    req = urllib.request.Request(url)
    res = Exec_api ()
    body = res.exec (req)
    print (json.dumps(body, indent=4))
    return 0

def auth_test ():
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
    print (json.dumps(body, indent=4))
    return 0

def incoming_webhook (argv:list):
    """
    use incoimng-webhook
    incoming-webhook は結果をjsonで返さないので、これだけ特殊処理
    """
    res = Exec_api ()
    res.conf ()
    message = str(argv[0])
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
    return 0

def post (argv:list):
    """
    https://api.slack.com/methods/chat.postMessage
    """
    res = Exec_api ()
    res.conf ()
    message = str(argv[0])
    method = "POST"
    headers = {
        "Content-Type": "application/json",
    }
    url = "https://slack.com/api/chat.postMessage?token=" + token + "&channel=" + channel + "&text=" + message
    req = urllib.request.Request (url, method=method, headers=headers)
    body = res.exec (req)
    print (json.dumps(body, indent=4))
    return 0

def conv_list (argv:list):
    """
    https://api.slack.com/methods/conversations.list
    default:
        types: public, private
        exclude_archived: true
    """
    # options
    types = "public_channel,private_channel"
    exclude_archived = "true"

    if argv[0:1]:
        if argv[0] == "public":
            types = "public_channel"
        elif argv[0] == "private":
            types = "private_channel"
        else:
            types = "public_channel,private_channel"

    if argv[1:2]:
        if argv[1] == "true":
            exclude_archived = "true"
        elif argv[1] == "false":
            exclude_archived = "false"
        else:
            exclude_archived = "true"

    res = Exec_api ()
    res.conf ()
    api = "conversations.list"
    method = "GET"
    url = api_url + api
    params = {
        'token': token,
        'types': types,
        'exclude_archived': exclude_archived,
        'limit': 1000,
    }

    req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)), method=method)
    body = res.exec (req)
    print (json.dumps(body, indent=4))
    return 0

#def post_quote (message:str):
#    conf ()  
#    data = {
#        'text': "```" + message + "```"
#    }
#    headers = {
#        'Content-Type': 'application/json',
#    }
#    url = webhook_url
#    req = urllib.request.Request(url, json.dumps(data).encode(), headers)
#    with urllib.request.urlopen(req) as res:
#        body = res.read().decode('utf-8')
#    print ('ResponseBody:'+str(body), file=sys.stderr)
#
#    return 0
#
#def notice (message:str):
#    message = "notice: " + message
#    post (message)
#    return 0
#
#def warning (message:str):
#    message = "warning: " + message
#    post (message)
#    return 0
#
#def alert (message:str):
#    message = "alert: " + message
#    post (message)
#    return 0
#
