#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# =============================================
#      Author   : Andy Scout
#    E-mail     : andyhuzhill@gmail.com
#
#  Description  : Interface wrapper for tuling robot
#  Revision     : V1.0 2016/08/13
#
# =============================================

import requests
import json

api_url = "http://www.tuling123.com/openapi/api"
api_key = ""    # Replace this with your api_key


def __Enum(**enums):
    return type('Enum', (), enums)


RetCode = __Enum(
        Text=100000,
        Link=200000,
        News=302000,
        Menu=308000,
        Key_Error=40001,
        Empty_Info=40002,
        Request_TimeOut=4004,
        DataFormatError=40007)


class TuringRobot(object):
    def __init__(self, api_url, api_key):
        self._url = api_url
        self._key = api_key

    def post_message(self, message, userid=None, loc=None):
        msg = {}
        msg["key"] = self._key
        msg["info"] = message
        if userid is not None:
            msg["userid"] = userid

        if loc is not None:
            msg["loc"] = loc

        msg_return_data = requests.post(self._url, json.dumps(msg))
        msg_return = json.loads(msg_return_data.text)

#        print self._parse_return_message(msg_return)
        return self._parse_return_message(msg_return)

    def _parse_return_message(self, data):
        code = data["code"]
        result = ''

        if code == RetCode.Text:
            result = data["text"]
        elif code == RetCode.Link:
            result = data["text"] + ' ' + data["url"]
        elif code == RetCode.News:
            result = data["text"] + ' \n'
            for news in data["list"]:
                result += u"{0} {1} 来自 {2}\n\n".format(
                        news["article"],
                        news["detailurl"],
                        news["source"])

        elif code == RetCode.Menu:
            result = data["text"] + ' \n'
            for menu in data["list"]:
                result += u"菜名:{0} \n原料:{1} \n做法:{2}\n\n".format(
                        menu["name"],
                        menu["info"],
                        menu["detailurl"])
        else:
            result = data["text"]

        return result


if __name__ == "__main__":
    robot = TuringRobot(api_url, api_key)

    robot.post_message(u"你好")

    robot.post_message(u"小狗的图片")

    robot.post_message(u"鱼香肉丝怎么做")

    robot.post_message(u"我想看新闻")

    robot.post_message(u"北京到拉萨的火车")

    robot.post_message(u"明天北京到拉萨的火车")
