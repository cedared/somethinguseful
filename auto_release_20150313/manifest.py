#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    解析Android Manifest XML模块。
    方便来修改渠道号
"""

from xml.dom.minidom import parse
import sys

MANIFEST = "AndroidManifest.xml"
# __ANDORID_PATH = r"/home/holmes/android/android/mgyun/RomasterV2/trunk"
_ANDORID_PATH = r"/home/holmes/xy/docs"
_MANIFEST_PATH = _ANDORID_PATH + "/" + MANIFEST

_KEY_NAME_ = set(["xinyi_id"])

def add_key_name(key):
    if key and (not key in _KEY_NAME_):
        print("add key " + key)
        _KEY_NAME_.add(key)

def parse_manifest(dom):
    """
        解析manifest
    """
    elemes = dom.getElementsByTagName("meta-data")
    return elemes

def parse_meta_data(metas, num):
    """
        解析Meta-data元素，并修改成num
    """
    for m in metas:
        a_name = m.getAttribute("android:name")
        a_value = m.getAttribute("android:value")
        print "name %s , value %s" % (a_name, a_value)
        if a_name in _KEY_NAME_:
            modify_id(m, str(num))

def modify_id(element, id):
    """
        修改element的， android:value属性为 id
    """
    element.setAttribute("android:value", id)
    print "modify android:value to " + id
    # save()

def save(dom, file):
    """
        保存 Manifest xml
    """
    xml_file = open(file, "w")
    dom.writexml(xml_file)
    xml_file.close()

def modify_manifest(file, num):
    """
        修改一个Manifest 文件的 meta data的android:value的值为 num
    """
    dom = parse(file)
    parse_meta_data(parse_manifest(dom), num)
    save(dom, file)

def get_manifest_version(file):
    """
        获取Manifest中的版本信息.
        return (version_code, version_name)
    """
    dom = parse(file)
    manifest_nodes = dom.getElementsByTagName("manifest")
    version_name = ""
    version_code = 0
    if manifest_nodes.length > 0:
        manifest = manifest_nodes.item(0)
        version_code = manifest.getAttribute("android:versionCode")
        version_name = manifest.getAttribute("android:versionName")

    dom = None
    return (version_code, version_name)



if __name__ == '__main__':
    # main()
    print(sys.argv)
