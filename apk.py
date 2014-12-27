#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author: Albert<yangsong@2bapm.com>
#         http://2bapm.com
# Date: 2014-12-23 23:19
# Created on

import os

try:
    os.chdir('/Users/albert/Documents/channelcheck')
except OSError:
    print "Apk folder doesn't exsit"
    exit()

b = os.listdir('./')
if len(b) > 0:
    for each in b:
        if each[-4:] == '.apk':
            hexchannel = ""
            a = os.popen('/Users/albert/usr/bin/aapt d xmltree ' + '"' + each + '"' + ' AndroidManifest.xml').readlines()
            try:
                for index, each1 in enumerate(a):
                    if 'xinyi_id' in each1:
                        lines = index
            except:
                print "'" + each + "'" + " is not Xinyi's product\n"

            try:
                hexchannel = a[lines+1][-6:]
                decchannel = str(int(hexchannel.upper(), 16))
                print decchannel + " " + each + "\n"

            except:
                print "'" + each + "'" + " is not Xinyi's product\n"

else:
    print "There is no apks to check"




