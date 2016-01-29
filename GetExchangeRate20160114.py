#!/usr/bin/env python
# -*- coding:utf-8  -*-
__author__ = 'Kanny'

import os,sys,re
import urllib,urllib2
import json
import simplejson
import csv
import time
import types


Thresholdrate = 4.6
LastFile = r'LastRate.txt'
url = 'http://download.finance.yahoo.com/d/quotes.csv?s=AUDCNY=X&f=sl1d1t1ba&e=.csv'


### Wechat Corp ID,KEY
corp_id="wx1a00c43b0a1e71b5"
secret="mSWi2mQ-089ri3QIRuU6avNMwDfB9db1_ZaMNrnT_JWNUhnKrj2W4i9BCdKEZ1lI"

### Get Token
def GetToken(corp_id, secret):
    res = urllib2.urlopen('https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (corp_id, secret))
    res_dict = simplejson.loads(res.read())
    token = res_dict.get('access_token', False)
    return token

### Post Data To Wechat Server
def http_post(MSG):
    Tag_ID = '6'
    url='https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + GetToken(corp_id, secret)

    ### Send SMS By wechat user id
    values ={'totag':Tag_ID,'msgtype': 'text', 'agentid': '2', 'text': { 'content': MSG }, 'safe':'0' }

    jdata = json.dumps(values)
    req = urllib2.Request(url, jdata)
    response = urllib2.urlopen(req)
    return response.read()

def GetRate():
    f = urllib2.urlopen(url)
    with open('exchangerate.csv', 'w') as code:
          code.write(f.read())
    with open('exchangerate.csv', 'r') as f:
          reader = csv.reader(f)
          for row in reader:
               rate = row[1]
               return float(rate)


if __name__ == "__main__":
    NOWER = GetRate()
    TEXT = 'NOW AUD To CNY: %s' % str(NOWER)
    print TEXT
    print '===================================='

if os.path.exists(LastFile):
    if float(NOWER) < float(Thresholdrate):
        f = open(LastFile,'r')
        content = f.read()
        if float(NOWER) < float(content):
            TEXT = 'AUD To CNY: %s' % str(NOWER)
            http_post(TEXT)
            print 'Newest Rate Send To Webchat'
            f.close()
            f = open(LastFile,'w')
            f.write(str(NOWER))
            f.close()
        else:
            print 'Nowest Rate is not lower than that last time'
            f.close()
            f = open(LastFile,'w')
            f.write(str(NOWER))
            f.close()
    else:
         print 'Newest Rate is higher than Thresholdrate'
         sys.exit(0)
else:
    if float(NOWER) < float(Thresholdrate):
        TEXT = 'AUD To CNY: %s' % str(NOWER)
        http_post(TEXT)
        print 'Newest Rate Send To Webchat'
    else:
        print 'Newest Rate is higher than Thresholdrate'
    f = open(LastFile,'w')
    f.write(str(NOWER))
    f.close()
    sys.exit(0)