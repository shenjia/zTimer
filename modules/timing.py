import pygame
import random
import math
import time
from configs import constants as c
from modules import helpers
from modules import resources
from modules.timer import Timer
from sys import exit

class Timing():

    def __init__(self):
        pass

    def run(self):

        # 主循环
        while True:

            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                if event.type == pygame.KEYDOWN:
                    self.onKeyDown(event.key)

            # 更新并绘制画面
            self.update()
            self.draw()
            self.clock.tick(c.FPS)

    def update(self):

        # 更新计时器
        self.timer.update()

        # 播放滴答声
        if self.timer.isCounting:
            self.playMusic()
        else:
            pygame.mixer.music.stop()

    def draw(self):

        # 背景
        self.screen.fill(c.BLACK)

        # 显示计时器
        text = self.timer.getText()
        color = self.timer.getColor()
        size = self.timer.getFontSize()
        font = pygame.font.Font(c.TIMER_FONT, size)
        surface = font.render(text, True, color)
        position = surface.get_rect()
        position.center = self.screenCenter
        self.screen.blit(surface, position)

        # 版权信息
        font = pygame.font.Font(c.LICENSE_FONT, c.LICENSE_SIZE)
        surface = font.render(c.LICENSE_TEXT, True, c.LICENSE_COLOR)
        position = surface.get_rect()
        position.center = self.screenBottom
        self.screen.blit(surface, position)

        pygame.display.update()

    def setup(self):

        pygame.init()
        pygame.mixer.init()

        # 初始化屏幕
        self.screenResolution = pygame.display.list_modes()[0]
        self.screenWidth, self.screenHeight = self.screenResolution
        self.screenCenter = (self.screenWidth / 2, self.screenHeight / 2)
        self.screenBottom = (self.screenWidth / 2, self.screenHeight / 1.1)
        self.screen = pygame.display.set_mode(self.screenResolution, pygame.FULLSCREEN, 32)

        # 加载资源
        resources.loadAll()
        pygame.mixer.music.load(c.MUSIC_TICK)
        pygame.mixer.fadeout(200)
        self.clock = pygame.time.Clock()

        self.timer = Timer({
            'totalSeconds' : c.DEFAULT_SECONDS,
            'isCountDown' : True,
            'isHide' : True,
            'callback' : self.playAlarm
        })

    def playAlarm(self):
        pygame.mixer.music.stop()
        resources.AUDIOS['alarm'].play()

    def playMusic(self):

        volume = self.getVolume()
        pygame.mixer.music.set_volume(volume)        
        
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(loops=1)

    def getVolume(self):

        # 前几秒渐变
        gap = 60 - self.timer.remainSeconds
        ratio = gap / c.COUNTING_ZOOM_IN_SECONDS 
        return c.COUNTING_VOLUME if ratio > 1 else c.COUNTING_VOLUME * ratio

    def onKeyDown(self, key):

        # ESC：关闭
        if (key == pygame.K_ESCAPE):
            self.exit()

        # SPACE：开始 / 暂停
        if (key == pygame.K_SPACE):
            if self.timer.isRunning:
                self.timer.stop()
            elif self.timer.isOver:
                self.setup()
            else:
                self.timer.start()

        # ENTER：重置
        if (key == pygame.K_RETURN):
            self.setup()

        # +：放大字体
        if (key == pygame.K_EQUALS or key == pygame.K_KP_PLUS):
            self.zoomIn()

        # -：缩小字体
        if (key == pygame.K_MINUS or key == pygame.K_KP_MINUS):
            self.zoomOut()

        # 上 / 左：增加时间
        if (key == pygame.K_UP or key == pygame.K_LEFT):
            self.timer.plus()

        # 下 / 右：减少时间
        if (key == pygame.K_DOWN or key == pygame.K_RIGHT):
            self.timer.minus()

    def zoomIn(self):
        self.timer.zoomRatio = self.timer.zoomRatio * (1 + c.FONT_ZOOM_RATIO)

    def zoomOut(self):
        self.timer.zoomRatio = self.timer.zoomRatio * (1 - c.FONT_ZOOM_RATIO)

    def exit(self):
        exit()

timing = Timing()
