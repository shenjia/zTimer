import os
import pygame
from configs import constants as c
from .helpers import *

AUDIOS = {}

# 加载音效
def loadAudio(dir, file, name):
    AUDIOS[name] = pygame.mixer.Sound(os.path.join(dir, file))

# 加载所有资源
def loadAll():
    walk(abspath('resources', 'audios'), loadAudio, c.AUDIO_EXTS)