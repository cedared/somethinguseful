#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import commands
import sys
import os
import manifest as mf
import shutil
import time
import plugin_bridge


class Config:
    """
        配置
        config.json
        {
            "projects": ["Romaster", "AppCool", "RomasterSu"],
            "paths":{
                "Launcher8":"/home/holmes/android/android/mgyun/Launcher8/branches/ModuleLauncher"
            },
            "build": 0
        }
    """
    def __init__(self, conf):
        self._projects = tuple(conf["projects"])
        self._build_index = conf["build"]
        self._project_paths = conf["paths"]
        
    def get_build_index(self):
        """
            获取build的index
        """
        return self._build_index
    
    def get_projects(self):
        """
            项目集合
        """
        return self._projects

    def get_build_project(self):
        """
            要编译的项目
        """
        if self._build_index < len(self._projects):
            return self._projects[self._build_index]
        else:
            return None

    def get_build_project_path(self):
        """
            要编译的项目路径
        """
        pro = self.get_build_project()
        if pro != None:
            return self._project_paths.get(pro, None)
        return None


_CONFIG_FILE = "config.json"
_project_list_ = None
_PROJECT_NAME_ = None
_PROJECT_DIRECTED_PATH = None

# 读取配置
if os.path.exists(_CONFIG_FILE):
    print("- Try to load config.json")
    import json
    config_file = file(_CONFIG_FILE)
    conf = json.load(config_file)
    config_file.close()
    config = Config(conf)
#     print(config.get_projects())
#     print(config.get_build_index())
#     exit(0)
    _project_list_ = config.get_build_project()
    _PROJECT_NAME_ = config.get_build_project()
    if _PROJECT_NAME_ == None:
        print("\"build\" index in config.json is no available.")
        exit(1)
    _PROJECT_DIRECTED_PATH = config.get_build_project_path()
else:
    # 没有配置
    # Romaster AppCool
    _project_list_ = ("Romaster", "AppCool", "RomasterSu")
    # the project name which want to release
    _PROJECT_NAME_ = _project_list_[2]
    

_PROJECT_FOLDER_NAME = None

# 确定项目的路径
if _PROJECT_DIRECTED_PATH != None:
    if os.path.isabs(_PROJECT_DIRECTED_PATH):
        _PROJECT_PATH_ = _PROJECT_DIRECTED_PATH
        _PROJECT_FOLDER_NAME = os.path.basename(_PROJECT_PATH_)
    else:
        _PROJECT_PATH_ = "project/" + _PROJECT_DIRECTED_PATH
        _PROJECT_FOLDER_NAME = os.path.basename(_PROJECT_PATH_)
else:
    _PROJECT_PATH_ = "project/" + _PROJECT_NAME_
    _PROJECT_FOLDER_NAME = _PROJECT_NAME_



_MANIFEST_FILE_ = "%s/%s" % (_PROJECT_PATH_, mf.MANIFEST)
_MANIFEST_FILE_STUDIO_ = "%s/src/main/%s" % (_PROJECT_PATH_, mf.MANIFEST)

_BUILID_XML_ = _PROJECT_PATH_ + "/build.xml"
_PROJECT_RELEASE_FILE_ = "%s/build/outputs/apk/%s-release.apk" % (_PROJECT_PATH_, _PROJECT_FOLDER_NAME)
_PROJECT_BIN_PATH_ = _PROJECT_PATH_ + "/bin"
_PROJECT_GEN_PATH_ = _PROJECT_PATH_ + "/gen"

# gradle 编译目录
_PROJECT_BUILD_PATH_ = _PROJECT_PATH_ + "/build"
_PROJECT_PROGUARD_PATH_ = _PROJECT_PATH_ + "/build/proguard"
_PROJECT_PROGUARD_DEST_PATH_ = _PROJECT_PATH_ + "/proguard"

# gradle 编译系统
_COMPILE_BIN_PATH_ = "/home/holmes/prosoft/gradle/gradle-2.2.1/bin/gradle"
# ant 编译系统
_ANT_PATH_ = "/home/holmes/prosoft/ant/bin"

# ant 编译命令
_RELEASE_CMD_ANT_ = "%s/ant -f %s release" % (_ANT_PATH_, _BUILID_XML_)
# 编译命令(gradle)
_RELEASE_CMD = "%s -q -p %s assembleRelease" % (_COMPILE_BIN_PATH_, _PROJECT_PATH_)

# add more meta key

mf.add_key_name("TD_CHANNEL_ID")
mf.add_key_name("UMENG_CHANNEL")

def get_time():
    return time.strftime("%y%m%d", time.localtime())

_RELEASE_DATE_ = get_time()


_current_manifest_path = None

def ensure_manifest():
    global _current_manifest_path
    if os.path.exists(_MANIFEST_FILE_):
        _current_manifest_path = _MANIFEST_FILE_
    elif os.path.exists(_MANIFEST_FILE_STUDIO_):
        _current_manifest_path = _MANIFEST_FILE_STUDIO_
    else:
        print("Mainfest no found.")
        exit(4)



def ant():
    """ ant 编译 """
    print("  --> ant")
    commands.getoutput(_RELEASE_CMD_ANT_)
    
def build_with_gradle():
    """ gradle 编译 """
    print("  --> gradle")
    commands.getoutput(_RELEASE_CMD)
    
def build():    
    """ 编译 """
    build_with_gradle()

def pack_apk(start = -1, end = -1):
    """
     打包APK
     从渠道 start ~ end
    """
    #print("%d %d" % (start, end))
    if start == -1:
        print("- release")
        build_and_copy()
    elif end > 0:
        if start > end:
            print("the end number is invaliable")
            return
        else:
            print("- release apk with num %d to %d" % (start, end))
            pack_apk_range(start, end)
    else :
        print("- release apk with num %d" % (start))
        pack_apk_range(start, start)


def pack_apk_range(start, end):
    """
        循环范围打包
    """
    for num in xrange(start, end + 1):
        pack_apk_channel(num)

def pack_apk_list(channel_list):
    """
        从渠道列表打包
    """
    list_len = len(channel_list)
    if list_len == 0:
        print("channel list is empty")
        exit(9)
    print(" - channel_list is:")
    print(channel_list)
    for i in range(list_len):
        num = int(channel_list[i])
        pack_apk_channel(num)


def pack_apk_channel(channel_num):
    """
        打一个渠道包
    """
    use_plugin(channel_num)
    print("+ will release %d ..." % (channel_num))
    modify_manifest(channel_num)
    build_and_copy(channel_num)

def use_plugin(num):
    """
        使用插件
    """
    project_path = _PROJECT_PATH_
    p = plugin_bridge.get_plugin(_PROJECT_NAME_, project_path, num, _current_manifest_path)
    if p != None:
        print("+ use plugin into")
        p.run()

def modify_manifest(num):
    """
        修改manifest文件中的渠道号
    """
    mf.modify_manifest(_current_manifest_path, num)

def build_and_copy(num = -1):
    """
        编译并且COPY编译好的apk到release目录
    """
    build()
    copy_apk(num)

def copy_apk(num = -1):
    """
        COPY编译好的apk到release目录
    """    
    print("  --> copy file")
    if not os.path.exists("release"):
        os.makedirs("release")

    version = mf.get_manifest_version(_current_manifest_path)
    release_file_name = "%s_%s_%s%s.apk" % (_PROJECT_NAME_, version[1], _RELEASE_DATE_, ("_" + str(num)) if num != -1 else "")
    shutil.copyfile(_PROJECT_RELEASE_FILE_, "release/" + release_file_name)


def delete_exist_folder(path):
    """
       删除存在的目录
    """
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors = True)

def delete_bin_folder():
    """
        删除编译目录
    """
    
    print("everything has done, now to delete bin and gen dirs")
    # save the proguard information
    delete_exist_folder(_PROJECT_PROGUARD_DEST_PATH_)
    shutil.copytree(_PROJECT_PROGUARD_PATH_, _PROJECT_PROGUARD_DEST_PATH_)

    delete_exist_folder(_PROJECT_BIN_PATH_)
    delete_exist_folder(_PROJECT_GEN_PATH_)
    delete_exist_folder(_PROJECT_BUILD_PATH_)
    print("delete finished!")


def prepare():
    """
        做准备
    """
    if not os.path.exists("project"):
        os.makedirs("project")

def load_channel_from_file(file_path):
    """
        从文件加载渠道号
    """
    if not os.path.exists(file_path):
        print("channel file no found.")
        exit(10)
    channel_file = open(file_path)
    channel_list = channel_file.readlines()
    channel_file.close()
    
    list_len = len(channel_list)
    for i in range(list_len):
        channel_list[i] = int(channel_list[i])

    return channel_list


def main():
    args = sys.argv
    args_len = len(args)
    s = -1
    e = -1
    is_load_from_file = False
    channel_file = None

    if args_len == 2:
        if args[1] == "-p":
            show_project()
        s = int(args[1])
    if args_len > 2:
        if args[1] == "-f":
            is_load_from_file = True
            channel_file = args[2]
        else:
            s = int(args[1])
            e = int(args[2])
    
    prepare()
    
    if not os.path.exists(_PROJECT_PATH_):
        print("Project \"%s\" no exists on path \"%s\"" % (_PROJECT_NAME_, _PROJECT_PATH_))
        exit(1)

    print("==== %s ====" % (_PROJECT_NAME_))
    ensure_manifest()
    if _current_manifest_path == None:
        print(" -- Manifest is None")
        exit(5)
    else:
        print(" -- Manifest: " + _current_manifest_path)

    if not is_load_from_file:
        pack_apk(s, e)
    else:
        channel_list = load_channel_from_file(channel_file)
        pack_apk_list(channel_list)


def show_project():
    print("The releaseing project is %s " % (_PROJECT_NAME_))
    exit(0)

if __name__ == "__main__":
    main()
