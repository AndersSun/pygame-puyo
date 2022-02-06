import pygame as pg

import os
from Animation import *
from Contants import *
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")
# functions to create our resources


def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)
    # image = image.convert()

    return image

def loadBgImg():
    fullImg = load_image("bg19.png")
    sub = fullImg.subsurface((0,0,1018,578))
    bgImg = pg.transform.smoothscale(sub, (screenWidth, screenHeight))
    return bgImg


size = (CELL_SIZE, CELL_SIZE)


def getRect(row, col):
    x = col * 72
    y = row * 72
    
    return [x, y, 68, 68]


def redInPiece():
    r1 = getRect(0, 0)
    r2 = getRect(9, 0)

    r = [(r1, 20), (r2, 20)]
    return r


def greenInPiece():
    r1 = getRect(1, 0)
    r2 = getRect(9, 1)
    r = [(r1, 20), (r2, 20)]
    return r


def blueInPiece():
    r1 = getRect(2, 0)
    r2 = getRect(9, 2)
    r = [(r1, 20), (r2, 20)]
    return r


def yellowInPiece():
    r1 = getRect(3, 0)
    r2 = getRect(9, 3)
    r = [(r1, 20), (r2, 20)]
    return r


def purpleInPiece():
    r1 = getRect(4, 0)
    r2 = getRect(9, 4)
    r = [(r1, 20), (r2, 20)]
    return r


def redBlow():
    r1 = getRect(0, 0)
    r2 = getRect(12, 0)
    r3 = getRect(10, 6)
    r4 = getRect(10, 7)
    r = [(r1, 10), (r2, 50), (r3, 5), (r4, 5)]
    return r
def greenBlow():
    r1 = getRect(1, 0)
    r2 = getRect(13, 0)
    r3 = getRect(10, 8)
    r4 = getRect(10, 9)
    r = [(r1, 10), (r2, 50), (r3, 5), (r4, 5)]
    return r
def blueBlow():
    r1 = getRect(2, 0)
    r2 = getRect(12, 2)
    r3 = getRect(10, 10)
    r4 = getRect(10, 11)
    r = [(r1, 10), (r2, 50), (r3, 5), (r4, 5)]
    return r
def yellowBlow():
    r1 = getRect(3, 0)
    r2 = getRect(13, 2)
    r3 = getRect(10, 12)
    r4 = getRect(10, 13)
    r = [(r1, 10), (r2, 50), (r3, 5), (r4, 5)]
    return r
def purpleBlow():
    r1 = getRect(4, 0)
    r2 = getRect(12, 4)
    r3 = getRect(10, 14)
    r4 = getRect(10, 15)
    r = [(r1, 10), (r2, 50), (r3, 5), (r4, 5)]
    return r     
class NoAnima():
    """没有动画，只有图片"""

    def __init__(self, img):
        self.img = img

    def blit(self, surface, pos):
        surface.blit(self.img, pos)


class PuyoAnima():
    def __init__(self):
        self.img = None

    def init(self):
        self.img = load_image(
            'Nintendo Switch - Puyo Puyo Tetris 2 - Aqua.png')
        self.redInPieceFrames = createFrames(self.img, redInPiece(), size)
        self.greenInPieceFrames = createFrames(self.img, greenInPiece(), size)
        self.blueInPieceFrames = createFrames(self.img, blueInPiece(), size)
        self.purpleInPieceFrames = createFrames(
            self.img, purpleInPiece(), size)
        self.yellowInPieceFrames = createFrames(
            self.img, yellowInPiece(), size)
        """爆炸"""
        self.redBlowUpFrames = createFrames(self.img, redBlow(), size)
        self.greenBlowUpFrames = createFrames(self.img, greenBlow(), size)
        self.blueBlowUpFrames = createFrames(self.img, blueBlow(), size)
        self.yellowBlowUpFrames = createFrames(self.img, yellowBlow(), size)
        self.purpleBlowUpFrames = createFrames(self.img, purpleBlow(), size)

        """具有连接效果的图片"""
        self.redInBoardImgs = self.createInBoardImgs(self.img, TXT_R)
        self.greenInBoardImgs = self.createInBoardImgs(self.img, TXT_G)
        self.blueInBoardImgs = self.createInBoardImgs(self.img, TXT_B)
        self.yellowInBoardImgs = self.createInBoardImgs(self.img, TXT_Y)
        self.purpleInBoardImgs = self.createInBoardImgs(self.img, TXT_P)

    def createRed(self):
        animation = NoAnima(self.redInPieceFrames[0][0])
        return animation

    def createRedInPiece(self, fr):
        animation = Animation(fr, self.redInPieceFrames, True)
        return animation

    def createGreen(self):
        animation = NoAnima(self.greenInPieceFrames[0][0])
        return animation

    def createGreenInPiece(self, fr):
        animation = Animation(fr, self.greenInPieceFrames, True)
        return animation

    def createBlue(self):
        animation = NoAnima(self.blueInPieceFrames[0][0])
        return animation

    def createBlueInPiece(self, fr):
        animation = Animation(fr, self.blueInPieceFrames, True)
        return animation

    def createPurple(self):
        animation = NoAnima(self.purpleInPieceFrames[0][0])
        return animation

    def createPurpleInPiece(self, fr):
        animation = Animation(fr, self.purpleInPieceFrames, True)
        return animation

    def createYellow(self):
        animation = NoAnima(self.yellowInPieceFrames[0][0])
        return animation

    def createYellowInPiece(self, fr):
        animation = Animation(fr, self.yellowInPieceFrames, True)
        return animation
    """爆炸的动画"""

    def createRedBlowUp(self, fr, callback=None):
        animation = Animation(fr, self.redBlowUpFrames, False, callback)
        return animation
    def createGreenBlowUp(self, fr, callback=None):
        animation = Animation(fr, self.greenBlowUpFrames, False, callback)
        return animation
    def createBlueBlowUp(self, fr, callback=None):
        animation = Animation(fr, self.blueBlowUpFrames, False, callback)
        return animation
    def createYellowBlowUp(self, fr, callback=None):
        animation = Animation(fr, self.yellowBlowUpFrames, False, callback)
        return animation
    def createPurpleBlowUp(self, fr, callback=None):
        animation = Animation(fr, self.purpleBlowUpFrames, False, callback)
        return animation

    def getInBoardRects(self, color):
        row = 0
        if color == TXT_R:
            row = 0
        elif color == TXT_G:
            row = 1
        elif color == TXT_B:
            row = 2
        elif color == TXT_Y:
            row = 3
        elif color == TXT_P:
            row = 4
        else:
            raise Exception("error")
        rects = []
        for col in range(0, 16):
            rect = getRect(row, col)
            rects.append(rect)
        return rects
    def createInBoardImgs(self, img, color):
        """创建在board中，具有连接效果的图片"""
        rects = self.getInBoardRects(color)
        imgs = []
        for rect in rects:
            sub = img.subsurface(rect)
            sub = pg.transform.smoothscale(sub, size)
            imgs.append(sub)
        return imgs
        
    def getInBoardImg(self, color, b):
        """获取在board中，具有连接效果的图片"""
        animation = None
        if color == TXT_R:
            animation = NoAnima(self.redInBoardImgs[b])
        elif color == TXT_G:
            animation = NoAnima(self.greenInBoardImgs[b])
        elif color == TXT_B:
            animation = NoAnima(self.blueInBoardImgs[b])
        elif color == TXT_Y:
            animation = NoAnima(self.yellowInBoardImgs[b])
        elif color == TXT_P:
            animation = NoAnima(self.purpleInBoardImgs[b])
        return animation
        
puyoAnima = PuyoAnima()
