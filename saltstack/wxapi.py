# -*- coding: utf-8 -*-

import json
import urllib
import urllib2


class WxAPI(object):
    def __init__(self, corpid, corpsecret):
        self.__url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?" \
                    "corpid=%(corpid)s&corpsecret=%(corpsecret)s" \
                    % {"corpid": corpid, "corpsecret": corpsecret}
        self.__token_id = self.getToken()

    def getToken(self):
        url = self.__url
        req = urllib2.Request(url)
        try:
            opener = urllib2.urlopen(req)
        except urllib2.HTTPError:
            raise urllib2.HTTPError
        content = json.loads(opener.read())
        try:
            token = content['access_token']
            return token
        except KeyError:
            raise KeyError

    def postRequest(self, touser, content):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?" \
            "access_token=%(access_token)s" \
            % {"access_token": self.__token_id}

        params = json.dumps({
                  "touser":  touser,
                  "msgtype": "text",
                  "agentid": 1,
                  "text": {
                        "content": content
                    },
                  "safe": "0"
                }, ensure_ascii=False)
        req = urllib2.Request(url, params)
        req.add_header('Content-Type', 'application/json')
        try:
            opener = urllib2.urlopen(req)
            result = json.loads(opener.read())
            if result.get('errcode') == 0:
                return {"errorcode": 0,
                        "res": "send msg successfully."}
            else:
                return {"errorcode": 1,
                        "res": "send msg failed."}
        except urllib2.HTTPError:
            raise urllib2.HTTPError
