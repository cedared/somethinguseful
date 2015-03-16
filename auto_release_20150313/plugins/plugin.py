#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import hashlib
import shutil

class Plugin(object):
    """
        插件
    """

    def __init__(self, project, path, channel, mainifest):
        """
            初始化插件,
            定义 项目，项目目录，渠道，mainifest文件path
        """
        self.project = project
        self.path = path
        self.channel  = channel
        self.mainifest = mainifest

    def run(self):
        """
            运行
        """
        pass


class iRootPlugin(Plugin):
    """
        root 大师的plugin
    """

    BASE_KING_PATH = "/home/holmes/xy/su/king_apk/mixed/2471"
    PROJECT_KING_NAME = "Kinguser"

    def __init__(self, project, path, channel, mainifest):
        Plugin.__init__(self, project, path, channel, mainifest)
        self.init_king_maps()
        self.project_king_path = self.path + "/src/main/assets/" + self.PROJECT_KING_NAME

    def init_king_maps(self):
        """
        03=1004
        23=2029
        93=2040
        53=2052

        渠道号与Kinguser的对应
        """
        self.king_map = {
            1004:"03",
            2029:"23",
            2040:"93",
            2052:"53"
        }


    def run(self):
        try:
            king_apk = self.king_map[self.channel];
        except KeyError, e:
            king_apk = None
            
        if king_apk != None:
            king_apk_path = self.BASE_KING_PATH + king_apk + "/" + self.PROJECT_KING_NAME
            self.check_king_apk(king_apk_path)
        else:
            # 还原正常渠道
            king_apk_path = self.BASE_KING_PATH + "02"+ "/" + self.PROJECT_KING_NAME
            self.check_king_apk(king_apk_path)

    def check_king_apk(self, king_apk_path):
        """
            检测king apk的md5
        """
        king_apk_md5 = None
        project_king_md5 = None

        apk_file = open(king_apk_path)
        king_apk_md5 = hashlib.md5(apk_file.read()).hexdigest()
        apk_file.close()

        apk_file = open(self.project_king_path)
        project_king_md5 = hashlib.md5(apk_file.read()).hexdigest()
        apk_file.close()

        if project_king_md5 != king_apk_md5:
            # print("change apk")
            print("apk md5 %s , project md5 %s" % (king_apk_md5, project_king_md5))
            self.change_apk(king_apk_path)
        else:
            print("the same king apk for " + str(self.channel))


    def change_apk(self, king_apk_path):
        """
            替换kinguser apk
        """
        shutil.copy2(king_apk_path, self.project_king_path)


if __name__ == '__main__':
    iroot_plugin = iRootPlugin("RomasterSu", "/home/holmes/My/py/py/android/project/RomasterSu", 1004, "")
    iroot_plugin.run()

