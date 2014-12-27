#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author: Albert<yangsong@2bapm.com>
# http://2bapm.com
# Date: 2014-11-12 14:11
# Created on My mac at work


import urllib2
import hmac
import hashlib
import time


def get_sig(cfg):

    str_filter = ".-_"
    code_url_addr = urllib2.quote(cfg['urlAddr'], str_filter)
    url_data2 = sorted(cfg['url_data'].iteritems(), key=lambda d: d[0])
    code_str0 = ""

    for (value01, value02) in url_data2:
        if code_str0:
            code_str0 += "&" + str(value01) + '=' + str(value02)
        else:
            code_str0 += str(value01) + '=' + str(value02)

    code_str1 = urllib2.quote(code_str0)
    code_conn = cfg['urlMethod'] + '&' + code_url_addr + '&' + code_str1
    sig = hmac.new(cfg['appkey'] + '&', code_conn, hashlib.sha1).digest().encode('base64').rstrip()

    return sig


def test():
    url_data = {'openid': '12345', 'openkey': '12345', 'pf': 'wanba_ts', 'appid': 12345, 'format': 'json', 'user_attr': '{"level":%d}' % 1234}
    urlcfg = {'urlAddr': '/v3/user/set_achievement', 'urlMethod': 'GET', 'appkey': 'ABCDWFSFFG', 'url_data': url_data	}
    url_data['sig'] = get_sig(urlcfg)
    print(url_data)

if __name__ == '__main__':

    test()