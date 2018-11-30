import math
import pygame
import sys, os

# 处理pyinstaller的路径映射
ROOT = sys._MEIPASS if hasattr(sys, 'frozen') else os.getcwd()

# 生成路径
def abspath(*path):
    return os.path.join(ROOT, *path)

# 遍历一个目录里的文件
def walk(dir, walker, exts=()):
    for file in os.listdir(dir):
        name, ext = os.path.splitext(file)
        if ext.lower() in exts:
            walker(dir, file, name)
