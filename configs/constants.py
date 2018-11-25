import pygame

# 颜色配置
BLACK = (38, 38, 38)
GRAY = (117, 123, 129)
WHITE = (255, 255, 255)
GREEN = (80, 182, 69)
YELLOW = (255, 193, 0)
ORANGE = (251, 114, 6)
RED = (255, 0, 0)

# 计时器
TIMER_FONT = 'resources/fonts/Consolas Bold.ttf'
TIMER_SIZE = 420
TIMER_UP = 'TIME UP!'
TIMER_UP_SIZE = 300
FONT_ZOOM_RATIO = 0.07
DEFAULT_SECONDS = 600
WARNING_RATIO = 0.3
COUNTING_FONT_ZOOM_IN_RATIO = 1.5
COUNTING_ZOOM_IN_SECONDS = 50
COUNTING_VOLUME = 0.5
FPS = 30

# 版权信息
LICENSE_FONT = 'resources/fonts/Consolas.ttf'
LICENSE_TEXT = 'zTimer v1.0 @ zhangshenjia'
LICENSE_COLOR = GRAY
LICENSE_SIZE = 20

# 事件
EVENT_START = pygame.USEREVENT + 1
EVENT_STOP = pygame.USEREVENT + 2
EVENT_OVER = pygame.USEREVENT + 3

# 资源相关
IMAGE_EXTS = ('.png', '.jpg', 'bmp')
AUDIO_EXTS = ('.wav', '.ogg')
MUSIC_TICK = 'resources/audios/tick.ogg'
