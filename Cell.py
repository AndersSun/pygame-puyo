import pygame as pg

import Contants
from Contants import *
from frameRunner.FrameRunner import FrameRunner
from PuyoAnima import puyoAnima
# classes for our game objects


class Cell(pg.sprite.Sprite):
    """cell in board,每个格子有坐标信息和颜色 """

    def __init__(self, row, col, color):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        # 是否正在运动
        self.moving = False
        self.bgcolor = (255,0,0,0)
        self.image = pg.Surface((Contants.CELL_SIZE, Contants.CELL_SIZE))
        self.image = self.image.convert_alpha()
        self.image.fill(self.bgcolor)
        # self.image.set_colorkey(self.bgcolor)
        if(color not in Contants.TXT_COLORS):
            raise "aa"
        
        self.row = row
        self.col = col
        self.color = color
        self.fr = FrameRunner()

        self.anima = self.createDefaultAnima()

        x = self.col * Contants.CELL_SIZE
        y = self.row * Contants.CELL_SIZE

        self.rect = pg.Rect(x, y, Contants.CELL_SIZE, Contants.CELL_SIZE)
    def createDefaultAnima(self):
        """默认的动画"""

        if self.color == TXT_R:
            return puyoAnima.createRed()
        elif self.color == TXT_G:
            return puyoAnima.createGreen()
        elif self.color == TXT_B:
            return puyoAnima.createBlue()
        elif self.color == TXT_P:
            return puyoAnima.createPurple()
        elif self.color == TXT_Y:
            return puyoAnima.createYellow()

    def setInPieceImage(self):
        """在下落时的动画，副的cell会一闪一闪"""

        self.anima = self.createInPieceAnima()
    def createInPieceAnima(self):
        """在piece中的动画"""

        if self.color == TXT_R:
            return puyoAnima.createRedInPiece(self.fr)
        elif self.color == TXT_G:
            return puyoAnima.createGreenInPiece(self.fr)
        elif self.color == TXT_B:
            return puyoAnima.createBlueInPiece(self.fr)
        elif self.color == TXT_P:
            return puyoAnima.createPurpleInPiece(self.fr)
        elif self.color == TXT_Y:
            return puyoAnima.createYellowInPiece(self.fr)

    def setBlowUpAnima(self, callback):
        """在爆炸时的动画"""

        if self.color == TXT_R:
            self.anima = puyoAnima.createRedBlowUp(self.fr, callback)
        elif self.color == TXT_G:
            self.anima = puyoAnima.createGreenBlowUp(self.fr, callback)
        elif self.color == TXT_B:
            self.anima = puyoAnima.createBlueBlowUp(self.fr, callback)
        elif self.color == TXT_P:
            self.anima = puyoAnima.createPurpleBlowUp(self.fr, callback)
        elif self.color == TXT_Y:
            self.anima = puyoAnima.createYellowBlowUp(self.fr, callback)
    def setInBoardAnima(self, b):
        """设置落到board中的图片
            b是一个4位二进制数，表示和周围方块的关系
            4位分别表示左右上下
        """
        self.anima = puyoAnima.getInBoardImg(self.color, b)


    def fallDown(self, destRow, success=None):
        """向下跌落，当消除以后，或者不受用户控制以后发生"""
        self.moveto(destRow, self.col, FRAME_PER_CELL_FALLDOWN, success)

    def moveleft(self, destCol, framePerCell, success=None):
        """ 向左移动到指定列，使用指定的速度 """
        """ framePerCell 为使用多少帧走一个格子，越大越慢"""
        self.moveto(self.row, destCol, framePerCell, success)

    def moveright(self, destCol, framePerCell, success=None):
        """ 向右移动到指定行，使用指定的速度 """
        """ framePerCell 为使用多少帧走一个格子，越大越慢"""
        self.moveto(self.row, destCol, framePerCell, success)

    def movedown(self, destRow, framePerCell, success=None):
        """ 向下移动到指定行，使用指定的速度 """
        """ framePerCell 为使用多少帧走一个格子，越大越慢"""
        self.moveto(destRow, self.col, framePerCell, success)

    def moveto(self, destRow, destCol, framePerCell, success=None):
        """移动到目标行列"""
        """ framePerCell 为使用多少帧走一个格子，越大越慢"""
        if(self.moving):
            return
        self.moving = True
        self._moveto(destRow, destCol, framePerCell, success)

    def _moveto(self, destRow, destCol, framePerCell, success=None):
        """移动到目标行列"""
        """ framePerCell 为使用多少帧走一个格子，越大越慢"""
        stepRow = 0
        if(destRow > self.row):  # 向下移动
            stepRow = 1
        elif destRow < self.row:  # 向上移动
            stepRow = -1
        stepCol = 0
        if(destCol > self.col):  # 向右移动
            stepCol = 1
        elif destCol < self.col:  # 向左移动
            stepCol = -1

        def callback():
            # 达到目标
            if self.col == destCol and self.row == destRow:
                self.moving = False
                if success is not None:
                    success()
            else:
                self._moveto(destRow, destCol, framePerCell, success)

        self.stepOneCell(stepRow, stepCol, framePerCell, callback)

    def stepOneCell(self, stepRow, stepCol, framePerCell, callback=None):
        "移动1个格子，完成后调用回掉函数"
        "stepRow:y轴移动的方向,取值为0,-1,1"
        "stepCol:x轴移动的方向,取值为0,-1,1"

        # 先移动半格
        def moveHalf():
            self.rect.move_ip(stepCol*0.5*CELL_SIZE,
                              stepRow*0.5*CELL_SIZE)
        self.fr.setTimeout(moveHalf, framePerCell//2)

        # 再移动一格
        def moveOne():
            self.rect.move_ip(stepCol*0.5*CELL_SIZE,
                              stepRow*0.5*CELL_SIZE)
            self.col += stepCol
            self.row += stepRow
            if(callback is not None):
                callback()

        self.fr.setTimeout(moveOne, framePerCell)

    def blowUp(self, callback):
        """消除时的动画，先闪两下，然后播放爆炸的动画，完成后调用回掉函数"""
        self.moving = True
        # self.image.fill((0, 0, 0))
        # self.fr.setTimeout(lambda: self.image.fill((100, 100, 100)), 20)
        # self.fr.setTimeout(lambda: self.image.fill((255, 255, 255)), 60)
        def finished():
            self.moving = False
            callback()

        self.setBlowUpAnima(finished)
        # self.fr.setTimeout(finished, 61)

    def setRowCol(self,row, col):
        self.row = row
        self.col = col
        x = self.col * Contants.CELL_SIZE
        y = self.row * Contants.CELL_SIZE

        self.rect = pg.Rect(x, y, Contants.CELL_SIZE, Contants.CELL_SIZE)
    def update(self):
        """update"""
        self.image.fill(self.bgcolor)
        self.fr.update()
        self.anima.blit(self.image,(0,0))
    def clone(self):
        nc = Cell(self.row, self.col, self.color)
        return nc        
        
