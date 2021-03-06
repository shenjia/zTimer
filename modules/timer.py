import pygame
import math
from configs import constants as c

class Timer:

    template = {
        'since' : 0,
        'until' : 0,
        'now' : 0,
        'zoomRatio' : 1,
        'screenWidth' : 1440,
        'totalSeconds' : 0,
        'remainSeconds' : 0,
        'isReady': True,
        'isRunning' : False,
        'callback' : None,
    }

    def __init__(self, config):
        config = dict(self.template, **config)
        for key in config:
            setattr(self, key, config[key])
        self.until = self.since + self.totalSeconds * 1000
        self.remainSeconds = self.totalSeconds

    def start(self):
        self.isReady = False
        self.isRunning = True
        self.since = pygame.time.get_ticks()
        self.until = self.since + self.remainSeconds * 1000

    def stop(self):
        self.isRunning = False

    def plus(self, minutes = 1):

        # 不能超过一天
        if self.remainSeconds > 86400:
            return

        # 时间到了之后不能再调整
        if self.isTimeup:
            return

        # 一分钟以下以秒为单位
        if self.isCounting:
            seconds = minutes

        # 其他情况以一分钟为单位
        else:
            seconds = 60 * minutes

        self.remainSeconds = self.remainSeconds + seconds
        self.until = self.until + seconds * 1000
        if self.isReady:
            self.totalSeconds = self.totalSeconds + seconds

    def minus(self, minutes = 1):

        # 时间到了之后不能再调整
        if self.isTimeup:
            return

        # 一分钟以内按秒为单位
        if self.remainSeconds <= 60:
            seconds = minutes

        # 其他时间以分钟为单位进行调整
        else:
            seconds = 60 * minutes

        # 不能出现负数
        if seconds >= self.remainSeconds:
            return

        self.remainSeconds = self.remainSeconds - seconds
        self.until = self.until - seconds * 1000
        if self.isReady:
            self.totalSeconds = self.totalSeconds - seconds

    def update(self):
        if self.isRunning:
            self.now = pygame.time.get_ticks()
            self.remainSeconds = (self.until - self.now) / 1000
            if self.remainSeconds <= 0:
                self.remainSeconds = 0
                self.isRunning = False
                if self.callback != None:
                    self.callback()

    @property
    def percent(self):
        return self.remainSeconds / self.totalSeconds

    @property
    def fontSize(self):

        # 时间到 / 一小时以上，用小字体
        if self.isTimeup or self.remainSeconds >= 3600:
            fontSize = self.screenWidth * c.SMALLER_FONT_RATIO
        else:
            fontSize = self.screenWidth * c.BIGGER_FONT_RATIO

        # 读秒时加大字体
        if self.isCounting:
            fontSize = fontSize * c.COUNTING_FONT_ZOOM_IN_RATIO

        return math.ceil(fontSize * self.zoomRatio)

    @property
    def color(self):

        # 未开始：绿色
        if self.isReady:
            return c.GREEN

        # 时间到：红色
        if self.isTimeup:
            return c.RED

        # 暂停状态：灰色
        if not self.isRunning:
            return c.GRAY

        # 读秒阶段：红色
        if self.isCounting:
            return c.RED

        # 提醒阶段：橙色
        if self.remainSeconds < self.totalSeconds * c.WARNING_RATIO:
            return c.ORANGE

        # 正常计时：黄色
        return c.YELLOW

    @property
    def text(self):

        # 时间到
        if self.isTimeup:
            return c.TIMER_UP

        # 读秒
        if self.isCounting:
            return str(math.ceil(self.remainSeconds))

        # 一小时以内
        elif self.remainSeconds < 3600:
            minutes = math.floor(math.ceil(self.remainSeconds) / 60)
            seconds = math.ceil(self.remainSeconds - minutes * 60)
            return str(minutes) + ':' + str(seconds).zfill(2)

        # 一小时以上
        else:
            minutes = math.floor(math.ceil(self.remainSeconds) / 60)
            seconds = math.ceil(self.remainSeconds - minutes * 60)
            hours = math.floor(math.ceil(minutes) / 60)
            minutes = math.ceil(minutes - hours * 60)
            return str(hours) + ':' + str(minutes).zfill(2) + ':' + str(seconds).zfill(2)

    @property
    def isCounting(self):
        return self.remainSeconds > 0 and self.remainSeconds < 60

    @property
    def isTimeup(self):
        return self.remainSeconds <= 0
