#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from plugins import plugin

_PROJECT_ROOT_ = "RomasterSu"
_PROJECT_ROOT_SPLIT_ = "RomasterSu_split"

def get_plugin(project, path, channel, manifest_path):
    """
        获取一个plugin处理器
    """

    if project == _PROJECT_ROOT_ or project == _PROJECT_ROOT_SPLIT_:
        return plugin.iRootPlugin(project, path, channel, manifest_path)

    return None


if __name__ == '__main__':
    p = get_plugin("RomasterSu", "/home/holmes/My/py/py/android/project/RomasterSu", 1004, "")
    if p != None:
        p.run()