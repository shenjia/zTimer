import pygame
import math
from configs import constants as c

class Timer:

    template = {
        'since' : 0,
        'until' : 0,
        'now' : 0,
        'zoomRatio' : 1,
        'totalSeconds' : 0,
        'remainSeconds' : 0,
        'isReady': True,
        'isRunning' : False,
        'isOver': False,
        'callback' : None
    }

    def __init__(self, config):
        config = dict(self.template, **config)
        for key in config:
            setattr(self, key, config[key])
        self.until = self.since + self.totalSeconds * 1000
        self.remainSeconds = self.totalSeconds
        self.fontSize = c.TIMER_SIZE

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
        if self.isOver:
            return

        # 一分钟以下取整到一分钟
        if self.isCounting:
            seconds = 60 - self.remainSeconds

        # 其他情况以一分钟为单位调整
        else:
            seconds = 60 * minutes

        self.remainSeconds = self.remainSeconds + seconds
        self.until = self.until + seconds * 1000
        if self.isReady:
            self.totalSeconds = self.totalSeconds + seconds
        
    def minus(self, minutes = 1):

        # 时间到了之后不能再调整
        if self.isOver:
            return

        # 一分钟以内不允许调整
        if self.isCounting:
            return

        # 最少调整为一分钟
        if self.remainSeconds - 60 * minutes < 60:
            seconds = self.remainSeconds - 60

        # 其他时间以一分钟为单位进行调整
        else:
            seconds = 60 * minutes

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
                self.isOver = True
                if self.callback != None:
                    self.callback()

    def getFontSize(self):
        fontSize = self.fontSize
        # 读秒时加大字体
        if self.isCounting:
            fontSize = fontSize * c.COUNTING_FONT_ZOOM_IN_RATIO
        # 时间到时锁定字体
        if self.isTimeup:
            fontSize = c.TIMER_UP_SIZE
        return math.ceil(fontSize * self.zoomRatio)

    def getPercent(self):
        return self.remainSeconds / self.totalSeconds

    def getColor(self):

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


    def getText(self):
        
        # 时间到
        if self.isTimeup:
            return c.TIMER_UP

        # 读秒计时
        if self.isCounting:
            return str(math.ceil(self.remainSeconds))
        
        # 分钟计时
        else:
            minutes = math.floor(math.ceil(self.remainSeconds) / 60)
            seconds = math.ceil(self.remainSeconds - minutes * 60)
            return str(minutes) + ':' + str(seconds).zfill(2)

    @property
    def isCounting(self):
        return self.remainSeconds > 0 and self.remainSeconds < 60
    
    @property
    def isTimeup(self):
        return self.remainSeconds <= 0