import math
import pygame
import sys, os

# 处理pyinstaller的路径映射
ROOT = sys._MEIPASS if hasattr(sys, 'frozen') else os.getcwd()

def clamp(value, min, max):
# 将值限制在一个范围内
    if value < min: return min
    if value > max: return max
    return value

# 计算两点之间的距离
def distance(x, y, Px, Py):
    return math.sqrt(math.pow(x - Px, 2) + math.pow(y - Py, 2))

# 生成路径
def abspath(*path):
    return os.path.join(ROOT, *path)

# 遍历一个目录里的文件
def walk(dir, walker, exts=()):
    for file in os.listdir(dir):
        name, ext = os.path.splitext(file)
        if ext.lower() in exts:
            walker(dir, file, name)
