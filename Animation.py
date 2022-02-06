import pygame as pg

def createBySheetPath(fr, bigImgPath, rectAndTimeout, loop, size):
    img = pg.image.load(bigImgPath)

    return createBySheet(fr, img, rectAndTimeout, loop, size)


def createFrames(img, rectAndTimeout, size):
    frames = []
    for e in rectAndTimeout:
        rect = e[0]
        timeout = e[1]
        sub = img.subsurface(rect)
        sub = pg.transform.smoothscale(sub, size)
        frames.append([sub, timeout])
    return frames


def createBySheet(fr, img, rectAndTimeout, loop, size):
    frames = createFrames(img, rectAndTimeout, loop, size)
    return Animation(fr, frames, loop)


class Animation():
    """播放动画 """

    def __init__(self, fr, frames, loop, callback=None):
        """frames是一个二维数组，每个数组元素有两项，第一项为img,第二项为时间
            当非循环的动画播放完时，会调用callback
        """
        self.fr = fr
        self.frames = frames
        self.loop = loop
        self.img = None
        # 第一个元素是序号
        c = [0]

        def showPic():
            index = c[0]
            if c[0] >= len(frames):#不循环的情况
                if loop:
                    raise Exception("error")
                else:
                    if callback is not None:
                        callback()
                return
            frame = frames[index]
            self.img = frame[0]
            timeout = frame[1]

            fr.setTimeout(lambda: showPic(), timeout)

            c[0] += 1
            if c[0] == len(frames):
                if loop:
                    c[0] = 0
                    
        showPic()

    def blit(self, surface, pos):
        surface.blit(self.img, pos)
