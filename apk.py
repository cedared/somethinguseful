#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author: Albert<yangsong@2bapm.com>
#         http://2bapm.com
# Date: 2014-12-23 23:19
# Created on

import os
import re

try:
    os.chdir('/Users/albert/Documents/channelcheck')
except OSError:
    print "Apk folder doesn't exsit"
    exit()

print "信壹\t友盟\t版本码\t版本名\t包名\t\t文件名"
print "================================================================================"
b = os.listdir('./')
if len(b) > 0:
    for each in b:
        if each[-4:] == '.apk':
            hexchannel_UM = ""
            hexchannel_xy = ""
            manifest = os.popen('/Users/albert/usr/bin/aapt d xmltree ' + '"' + each + '"' + ' AndroidManifest.xml').readlines()
            badging = os.popen('/Users/albert/usr/bin/aapt d badging ' + '"' + each + '"').readlines()
            try:
                for index, each1 in enumerate(manifest):
                    if 'xinyi_id' in each1:
                        lines_xy = index
                    if 'UMENG_CHANNEL' in each1:
                        lines_UM = index
            except:
                print "'" + each + "'" + " is not Xinyi's product\n"

            hexchannel_xy = manifest[lines_xy+1][-6:]
            decchannel_xy = str(int(hexchannel_xy.upper(), 16))
            hexchannel_UM = manifest[lines_UM+1][-6:]
            decchannel_UM = str(int(hexchannel_UM.upper(), 16))
            packagename = re.findall(r'=\'(\S*)\'', badging[0])[0]
            vcode = re.findall(r'=\'(\S*)\'', badging[0])[1]
            vname = re.findall(r'=\'(\S*)\'', badging[0])[2]
            print decchannel_xy + "\t" + decchannel_UM + "\t" + vcode + "\t" + vname + "\t" + packagename + "\t" + each + "\n"

        else:
            print each + " is not a apk file\n"

else:
    print "There is no files to check"




