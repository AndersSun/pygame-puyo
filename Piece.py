import pygame as pg
from random import choice

from Contants import *
from Cell import Cell
# classes for our game objects
# 转到上面,row -1，col不变
ANGLE_TOP = (-1, 0)
TO_TOP = 0
# 转到左面
ANGLE_LEFT = (0, -1)
TO_LEFT = 1
# 转到下面
ANGLE_BOTTOM = (1, 0)
TO_BOTTOM = 2
# 转到右面
ANGLE_RIGHT = (0, 1)
TO_RIGHT = 3
CELL2_POS = [ANGLE_TOP, ANGLE_LEFT, ANGLE_BOTTOM, ANGLE_RIGHT]


class Piece():
    """一个下落的方块，由两个格子组成 """

    def __init__(self, cell1=None, cell2=None, theAngle=TO_TOP):
        """ 在中间的顶上，生成两个cell, 下面的是主，上面的是副
            旋转时，副围绕着主转
        """
        if cell1 is None:
            color1 = choice(TXT_COLORS)
            cell1 = Cell(1, 2, color1)
        if cell2 is None:
            color2 = choice(TXT_COLORS)
            cell2 = Cell(0, 2, color2)
        self.cell1 = cell1
        self.cell2 = cell2
        self._angle = theAngle

    def isMoving(self):
        m1 = self.cell1.moving
        m2 = self.cell2.moving
        return m1 or m2

    def isValid(self, cells):
        """位置是否合理"""
        # 在borad范围内
        if self.cell1.col < 0 or self.cell1.col >= BOARD_COL:
            return False
        if self.cell1.row < 0 or self.cell1.row >= BOARD_ROW:
            return False
        if self.cell2.col < 0 or self.cell2.col >= BOARD_COL:
            return False
        if self.cell2.row < 0 or self.cell2.row >= BOARD_ROW:
            return False
        # 没有被占领
        if(cells[self.cell1.row][self.cell1.col] != 0):
            return False
        if(cells[self.cell2.row][self.cell2.col] != 0):
            return False
        return True
    def correctPos(self, cells):
        """修正位置,如果左右旋转时，碰到边界，则向右或向左挪一格
        如果修正后的位置合法，则返回true"""
        if(self.isValid(cells)):
            return True
        elif(self.angle==TO_LEFT):
            self.tempStepRight()
            return self.isValid(cells)
        elif(self.angle==TO_RIGHT):
            self.tempStepLeft()
            return self.isValid(cells)
        else:
            return self.isValid(cells)

    def tempStepLeft(self):
        self.cell1.col -= 1
        self.cell2.col -= 1

    def stepLeft(self, rate = FRAME_PER_CELL_CONTROLL, success=None):
        """ 向左一格，使用指定的速度 """
        callback = self.wrapCallback(success)
        self.cell1.moveleft(
            self.cell1.col-1, rate, callback)
        self.cell2.moveleft(
            self.cell2.col-1, rate, callback)

    def tempStepRight(self):
        self.cell1.col += 1
        self.cell2.col += 1

    def stepRight(self, rate = FRAME_PER_CELL_CONTROLL, success=None):
        """ 向右移动一格，使用指定的速度 """
        callback = self.wrapCallback(success)
        self.cell1.moveright(
            self.cell1.col+1, rate, callback)
        self.cell2.moveright(
            self.cell2.col+1, rate, callback)

    def tempStepDown(self):
        self.cell1.row += 1
        self.cell2.row += 1

    def stepDown(self, rate = FRAME_PER_CELL_CONTROLL, success=None):
        """ 向下移动一格，使用指定的速度 """
        callback = self.wrapCallback(success)
        self.cell1.movedown(
            self.cell1.row+1, rate, callback)
        self.cell2.movedown(
            self.cell2.row+1, rate, callback)

    def wrapCallback(self, success):
        "调用两次，才会调用success回调函数"
        if success is None:
            return None
        c = [0]

        def callback():
            c[0] += 1
            if c[0] == 2:
                success()
        return callback

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, newAngle):
        self._angle = newAngle
        self._calcCell2()

    def update(self):
        """update"""
        self.cell1.update()
        self.cell2.update()

    def clone(self):
        c1 = self.cell1
        c2 = self.cell2
        nc1 = c1.clone()
        nc2 = c2.clone()
        newPiece = Piece(nc1, nc2, self._angle)
        return newPiece

    def draw(self, surface):
        """draw"""
        surface.blit(self.cell1.image, self.cell1.rect)
        surface.blit(self.cell2.image, self.cell2.rect)

    def drawAtPos(self, surface, pos):
        surface.blit(self.cell2.image, pos)
        surface.blit(self.cell1.image, (pos[0], pos[1]+CELL_SIZE))

    def _calcCell2(self):
        row = self.cell1.row + CELL2_POS[self._angle][0]
        col = self.cell1.col + CELL2_POS[self._angle][1]
        self.cell2.setRowCol(row, col)
    def _calcCell1(self):
        row = self.cell1.row
        col = self.cell1.col
        self.cell1.setRowCol(row, col)
    def calcLocation(self):
        self._calcCell1()
        self._calcCell2()
