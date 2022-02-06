

import time
from FrameRunner import FrameRunner
import pygame as pg


class GreetingPanel(pg.sprite.Sprite):
    """ """

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer

        self.fr = fr = FrameRunner()
        self.image = pg.Surface((700, 200))
        self.image.fill((0, 0, 0))
        self.image = self.image.convert()
        self.rect = self.image.get_rect(x=100, y=50)
        self.font = pg.font.Font(None, 64)
        # 每隔100个frame，说一句话

        fr.setTimeout(lambda: self.showText('hello'), 0)
        fr.setTimeout(lambda: self.showText('how are you'), 200)
        fr.setTimeout(lambda: self.showText('miss me?'), 400)
        c = [0]
        startTime = time.time()
        me = self
        def showFps():
            c[0] = c[0]+1
            nowTime = time.time()
            fps = c[0]//(nowTime - startTime)
            me.fpsText = me.font.render(str(fps), True, (255, 255, 255))
            me.fpsTextpos = me.text.get_rect(
                centerx=me.image.get_width()-50, y=10)

        fr.setInterval(showFps, 1)

    def update(self):
        """update"""

        self.fr.update()
        self.image.fill((0, 0, 0))
        if self.text is not None and self.textpos is not None:
            self.image.blit(self.text, self.textpos)
        if self.fpsText is not None and self.fpsTextpos is not None:
            self.image.blit(self.fpsText, self.fpsTextpos)

    def showText(self, text):
        self.text = self.font.render(text, True, (255, 255, 255))
        self.textpos = self.text.get_rect(
            centerx=self.image.get_width() / 2, y=10)
