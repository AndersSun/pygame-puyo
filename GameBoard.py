import pygame as pg
from pygame import rect

from Cell import Cell
from Contants import *
from Piece import Piece
from pygame.locals import *

from EraseCmd import canCellFalling, cellMoving
from EraseCmd import EraseCmd
from frameRunner.FrameRunner import FrameRunner
from calcScore import calcScore
# classes for our game objects


def blit_text(surface, textList, pos, font, color):

    x, y = pos
    for line in textList:
        word_surface = font.render(line, True, color)
        surface.blit(word_surface, (x, y))
        size = word_surface.get_size()
        y += size[1]


GS_RUNNING = "running"
GS_PAUSED = "paused"
GS_FINISHED = "finished"


class GameBoard(pg.sprite.Sprite):
    """game board class"""

    def __init__(self, x, y, leftPlayer):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        # 游戏板的大小是6*12个格子，每个格子的边长为50个像素，稍微比这个再大一点
        self.cellsFieldWidth = BOARD_COL * CELL_SIZE
        self.cellsFieldHeight = BOARD_ROW * CELL_SIZE

        self.topPanelWidth = self.cellsFieldWidth
        self.topPanelHeight = 30

        self.chainPanelWidth = self.cellsFieldWidth
        self.chainPanelHeight = 200

        self.height = self.topPanelHeight + self.cellsFieldHeight + self.chainPanelHeight

        self.leftPanelWidth = 3
        self.leftPanelHeight = self.height

        self.infoPanelWidth = 200
        self.infoPanelHeight = self.height

        self.width = self.leftPanelWidth+self.cellsFieldWidth+self.infoPanelWidth

        self.chainFont = pg.font.Font(None, 30)
        self.topFont = pg.font.Font(None, 30)
        self.scoreFont = pg.font.Font(None, 50)
        self.chainMsg = []
        # image是底板
        # cellsField是cell下落的地方，放在image里，处于中间
        # infoPanel 显示各种信息， 放在image里，靠右边
        # chainPanel显示连击信息，放在image里，靠下边
        self.image = pg.Surface((self.width, self.height)).convert_alpha()
        self.cellsField = pg.Surface(
            (self.cellsFieldWidth, self.cellsFieldHeight)).convert_alpha()
        self.leftPanel = pg.Surface(
            (self.leftPanelWidth, self.leftPanelHeight)).convert_alpha()
        self.infoPanel = pg.Surface(
            (self.infoPanelWidth, self.infoPanelHeight)).convert_alpha()
        self.topPanel = pg.Surface(
            (self.topPanelWidth, self.topPanelHeight)).convert_alpha()
        self.chainPanel = pg.Surface(
            (self.chainPanelWidth, self.chainPanelHeight)).convert_alpha()

        self.bgcolor = (100, 100, 100,100)

        # self.cellsField.set_colorkey((0,0,0))
        self.cellsField.fill(self.bgcolor)
        self.rect = (x, y, self.width, self.height)
        self.gameStatus = None

        self.leftPlayer = leftPlayer
        if leftPlayer:  # 双人时，左边的玩家
            self.leftKey = K_a
            self.rightKey = K_d
            self.topKey = K_w
            self.bottomKey = K_s
            self.rotateLeft = K_q
            self.rotateRight = K_e
        else:  # 双人时，右边的玩家
            self.leftKey = K_LEFT
            self.rightKey = K_RIGHT
            self.topKey = K_UP
            self.bottomKey = K_DOWN
            self.rotateLeft = K_k
            self.rotateRight = K_l

    def restartGame(self):
        """重新开始游戏"""
        # cell代表board中的格子,如果格子中有方块，则对应元素为Cell的实例
        # 如果格子是空的，则对应的元素为0
        self.cells = [[0 for c in range(0, BOARD_COL)]
                      for r in range(0, BOARD_ROW)]

        self.moveUp = False
        self.moveDown = False
        self.moveLeft = False
        self.moveRight = False

        self.eraseCmd = None

        self.piece = Piece()
        self.piece.cell1.setInPieceImage()

        """连续向左移动次数，第一次慢，后面会逐渐加快速度"""
        self.sustainLeftCount = 0
        self.sustainDownCount = 0
        self.sustainRightCount = 0
        self.npiece = Piece()
        self.nnpiece = Piece()

        self.fr = FrameRunner()
        self.freeDown()
        self.gameStatus = GS_RUNNING
        self.totalScore = 0

    def gameOver(self):
        self.gameStatus = GS_FINISHED

    def pauseGame(self):
        """暂停游戏"""
        self.gameStatus = GS_PAUSED

    def resumeGame(self):
        if self.gameStatus != GS_PAUSED:
            raise Exception("error")
        self.gameStatus = GS_RUNNING

    def handleEvent(self, event):
        if self.gameStatus != GS_RUNNING:
            return
        if(event.type == KEYDOWN):
            if event.key == self.topKey:
                pass
            elif event.key == self.bottomKey:
                self.moveDown = True
                self.moveUp = False
            elif event.key == self.leftKey:
                self.moveLeft = True
                self.moveRight = False
            elif event.key == self.rightKey:
                self.moveRight = True
                self.moveLeft = False
            # 旋转
            elif event.key == self.rotateLeft and self.piece is not None:
                
                for i in range(1, 4):
                    temp = self.piece.clone()
                    temp.angle = (self.piece.angle + i) % 4
                    if(temp.correctPos(self.cells)):
                        temp.calcLocation()
                        self.piece = temp
                        self.piece.cell1.setInPieceImage()
                        break

                
            elif event.key == self.rotateRight and self.piece is not None:
                for i in range(1, 4):
                    temp = self.piece.clone()
                    temp.angle = (self.piece.angle - i) % 4
                    if(temp.correctPos(self.cells)):
                        temp.calcLocation()
                        self.piece = temp
                        self.piece.cell1.setInPieceImage()
                        break

        elif event.type == KEYUP:
            if event.key == self.topKey:
                pass
            elif event.key == self.bottomKey:
                self.moveDown = False
                self.sustainDownCount = 0
            elif event.key == self.leftKey:
                self.moveLeft = False
                self.sustainLeftCount = 0
            elif event.key == self.rightKey:
                self.moveRight = False
                self.sustainRightCount = 0

    # 自由下落
    def freeDown(self):
        def func():
            if self.eraseCmd is None:
                if not cellMoving(self.cells):
                    if self._canPieceFalling():  # 没到底，就向下一格
                        temp = self.piece.clone()
                        temp.tempStepDown()
                        if(temp.isValid(self.cells)):
                            self.piece.stepDown()
                    else:  # 到底了
                        self.doErase()
        # 控制自由下落，每60帧一次
        self.fr.setInterval(func, FRAME_FREEDOWN)
    # 开始消除

    def doErase(self):
        # 如果不能下落，则开始消除
        self._movePieceToBoard()
        self.chainMsg = []

        def onErase(chainNum, links, score):
            """消除了一次"""
            self.chainMsg.append(str(chainNum)+" chain:"+str(score))

        def eraseFinished(chainNum, oneCmdScore):
            if(chainNum > 0):
                self.totalScore +=oneCmdScore
            self.eraseCmd = None
            self.piece = self.npiece
            self.piece.cell1.setInPieceImage()
            self.npiece = self.nnpiece
            self.nnpiece = Piece()
            self.setInBoardAnima()
            if(chainNum > 0):
                self.chainMsg.append("chain finished:"+str(oneCmdScore))
        self.eraseCmd = EraseCmd(self, onErase, eraseFinished)
        self.eraseCmd.fallDownAndErase()

    def setInBoardAnima(self):
        """设置每个落到board上的cell的图片"""
        for col in range(0, BOARD_COL):
            for row in range(0, BOARD_ROW):
                cell = self.cells[row][col]
                if(cell != 0):
                    self.setInBoardAnimaForCell(cell)

    def setInBoardAnimaForCell(self, cell):
        # 四位2进制数，分别表示左右上下
        b = 0b0000
        leftCell = self.getCell(cell.row, cell.col-1)
        if(leftCell != 0 and leftCell.color == cell.color):
            b = b | 0b1000
        rightCell = self.getCell(cell.row, cell.col+1)
        if(rightCell != 0 and rightCell.color == cell.color):
            b = b | 0b0100
        topCell = self.getCell(cell.row-1, cell.col)
        if(topCell != 0 and topCell.color == cell.color):
            b = b | 0b0010
        bottomCell = self.getCell(cell.row+1, cell.col)
        if(bottomCell != 0 and bottomCell.color == cell.color):
            b = b | 0b0001
        cell.setInBoardAnima(b)

    def update(self):
        """
            更新
        """
        if self.gameStatus == GS_RUNNING:
            self.fr.update()
            if self.cells[1][2] != 0:
                self.gameOver()
            elif self.eraseCmd is None:
                if not cellMoving(self.cells):
                    # 事件控制处理
                    self._userControll()
            self._drawToImage()

    def genTestData(self):
        self.cells[11][0] = Cell(11, 0, TXT_R)
        self.cells[10][0] = Cell(10, 0, TXT_R)
        self.cells[9][0] = Cell(9, 0, TXT_R)

        self.cells[11][1] = Cell(11, 1, TXT_G)
        self.cells[10][1] = Cell(10, 1, TXT_G)
        self.cells[9][1] = Cell(9, 1, TXT_G)
        self.cells[8][1] = Cell(8, 1, TXT_R)

    """返回指定格子的cell,如果没有或者超出范围，返回0"""

    def getCell(self, row, col):
        # 超出borad范围
        if col < 0 or col >= BOARD_COL:
            return 0
        if row < 0 or row >= BOARD_ROW:
            return 0
        c = self.cells[row][col]
        return c

    def _movePieceToBoard(self):
        self.cells[self.piece.cell1.row][self.piece.cell1.col] = self.piece.cell1.clone()
        self.cells[self.piece.cell2.row][self.piece.cell2.col] = self.piece.cell2.clone()
        self.piece = None

    def _canPieceFalling(self):
        if not canCellFalling(self.piece.cell1, self.cells):
            return False
        if not canCellFalling(self.piece.cell2, self.cells):
            return False
        return True

    def _userControll(self):
        if(self.piece is None):
            return
        if self.piece.isMoving():
            return
        if(self.moveDown):

            temp = self.piece.clone()
            temp.tempStepDown()
            if(temp.isValid(self.cells)):
                self.sustainDownCount += 1
                s = self.getSpeed(self.sustainDownCount)
                self.piece.stepDown(s)
        if(self.moveLeft):
            temp = self.piece.clone()
            temp.tempStepLeft()
            if(temp.isValid(self.cells)):
                self.sustainLeftCount += 1
                s = self.getSpeed(self.sustainLeftCount)
                self.piece.stepLeft(s)
        if(self.moveRight):
            temp = self.piece.clone()
            temp.tempStepRight()
            if(temp.isValid(self.cells)):
                self.sustainRightCount += 1
                s = self.getSpeed(self.sustainRightCount)
                self.piece.stepRight(s)

    def getSpeed(self, c):
        if c == 1:
            return 15
        elif c == 2:
            return 7
        else:
            return FRAME_PER_CELL_CONTROLL

    def _drawCellsField(self):
        # 先画板
        self.cellsField.fill(self.bgcolor)
        for row in range(0, BOARD_ROW):
            for col in range(0, BOARD_COL):
                cell = self.cells[row][col]
                if(cell != 0):
                    cell.update()
        for row in range(0, BOARD_ROW):
            for col in range(0, BOARD_COL):
                cell = self.cells[row][col]
                if(cell != 0):
                    self.cellsField.blit(cell.image, cell.rect)
        # 再画piece
        if(self.piece is not None):
            self.piece.update()
            self.piece.draw(self.cellsField)

    def _drawLeftPanel(self):
        self.leftPanel.fill((0, 255, 0, 100))

    def _drawInfoPanel(self):
        self.infoPanel.fill((0, 0, 255, 100))
        self.npiece.update()
        self.npiece.drawAtPos(self.infoPanel, (20, 20))
        self.nnpiece.update()
        self.nnpiece.drawAtPos(self.infoPanel, (20, 20+CELL_SIZE*3))
        scoreSurface = self.scoreFont.render(
            str(self.totalScore), True, (255, 0, 0))
        self.infoPanel.blit(scoreSurface, (40, 300))

    def _drawTopPanel(self):
        if self.leftPlayer:
            text = "move:a,s,d  rotate:q,e"
        else:
            text = "move:arrow keys  rotate:k,l"
        # print(text)
        word_surface = self.topFont.render(text, True, (255,0,0))
        self.topPanel.fill((255, 255, 0, 100))
        self.topPanel.blit(word_surface, (10, 0))

    def _drawChainPanel(self):
        self.chainPanel.fill((255, 255, 0, 100))

        if(self.chainMsg is not None):
            blit_text(self.chainPanel, self.chainMsg,
                      (10, 10), self.chainFont, (10, 10, 10))

    def _drawToImage(self):
        self._drawCellsField()
        self._drawLeftPanel()
        self._drawInfoPanel()
        self._drawTopPanel()
        self._drawChainPanel()

        self.image.fill((0, 100, 0, 100))

        self.image.blit(self.cellsField,
                        (self.leftPanelWidth, self.topPanelHeight))
        self.image.blit(self.leftPanel, (0, 0))
        self.image.blit(
            self.infoPanel, (self.leftPanelWidth+self.cellsFieldWidth, 0))
        self.image.blit(self.topPanel, (self.leftPanelWidth, 0))
        self.image.blit(self.chainPanel, (self.leftPanelWidth,
                        self.topPanelHeight+self.cellsFieldHeight))
