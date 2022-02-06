from Contants import *
from CountDownLatch import CountDownLatch
from calcScore import calcScore

""" cell 是否能继续下落"""


def canCellFalling(cell, cells):
    # 触底了
    if cell.row >= BOARD_ROW-1:
        return False
    # 下一格有东西
    if(cells[cell.row+1][cell.col] != 0):
        return False
    return True


"""cells 是否有在动的"""


def cellMoving(cells):
    for row in range(0, BOARD_ROW):
        for col in range(0, BOARD_COL):
            cell = cells[row][col]
            if(cell != 0 and cell.moving):
                return True
    return False


class EraseCmd():
    """描述一次清除puro的动作，
    一次清除指的是用户落下一个piece,引起的一次或多次清除"""

    def __init__(self, board, onErase, eraseFinished):
        self.chainNum = 0
        self.board = board
        self.onErase = onErase
        self.eraseFinished = eraseFinished
        # 是否已经完成消除的动作
        self.finished = False
        # 连击数
        self.chain = 0
        self.score = 0

    def fallDownAndErase(self):
        """下落所有cell,然后进行消除"""
        if(self.finished):
            raise "error"
        # 还有没有cell在动的，如果有，等它完成
        if self.cellMoving():
            raise Exception("不可能的")

        # 判断每个piece是否落到底了
        # 如果没有落到底的，就让他落到底
        # 从下往上判断，如果底下的能落下，则上面的一起落
        self.fallDownAllCells(lambda: self.eraseOneChain())

    def eraseOneChain(self):
        """消除一次,成功后检查是否还有能下落的，继续进行消除"""
        links = self.findToBeErasedCells()

        if(len(links) == 0):
            self.finished = True
            self.eraseFinished(self.chain, self.score)
        else:
            self.chain += 1
            theScore = calcScore(self.chain, links)
            self.score += theScore
            self.onErase(self.chain, links, theScore)
            self.eraseCells(lambda: self.fallDownAndErase())

    def fallDownAllCells(self, success):
        # 当所有的cell都掉下来，再调用回调函数
        latch = CountDownLatch(success)
        # 有多少个cell会下落的计数器
        fallCessNum = 0
        # 判断每个piece是否落到底了
        # 如果没有落到底的，就让他落到底
        # 从下往上判断，如果底下的能落下，则上面的一起落

        for col in range(0, BOARD_COL):
            # 计算这一列要下落多少格子
            failDownRow = 0
            for row in reversed(range(0, BOARD_ROW)):
                cell = self.board.cells[row][col]
                if(cell == 0):
                    failDownRow += 1
                elif failDownRow > 0:
                    fallCessNum += 1
                    self.board.cells[row][col] = 0
                    self.board.cells[cell.row+failDownRow][col] = cell
                    cell.fallDown(cell.row+failDownRow, latch.createCallback())
        if fallCessNum == 0:
            success()

    def eraseCells(self, success):
        """删掉所有连着的cell，完成动画后，调用success"""
        links = self.findToBeErasedCells()
        if len(links) == 0:
            success()
            return
        latch = CountDownLatch(success)
        for link in links:
            if len(link) < 4:
                raise "至少四个才能消"
            self.eraseOneLink(link, latch)

    def findToBeErasedCells(self):
        """找到所有可以被消除的cell,返回一个二维数组"""
        links = []
        for row in range(0, BOARD_ROW):
            for col in range(0, BOARD_COL):
                cell = self.board.cells[row][col]
                if(cell != 0 and not self._aleadyVisited(cell, links)):
                    link = []
                    self._visitForLink(cell, link)
                    if(len(link) > 1):
                        links.append(link)

        r = filter(lambda x: len(x) >= 4, links)

        return list(r)
    """判断cell是否已经遍历过了"""

    def _aleadyVisited(self, cell, links):
        for l in links:
            if cell in l:
                return True
        return False

    """在cells中查找cell周围相同颜色的link,并将其加入到link数组中"""

    def _visitForLink(self, cell, link):
        if cell in link:
            return
        link.append(cell)
        color = cell.color
        # 按照上左下右的顺序遍历
        topCell = self.board.getCell(cell.row-1, cell.col)
        if(topCell != 0 and topCell.color == color):
            self._visitForLink(topCell, link)

        leftCell = self.board.getCell(cell.row, cell.col-1)
        if(leftCell != 0 and leftCell.color == color):
            self._visitForLink(leftCell, link)

        bottomCell = self.board.getCell(cell.row+1, cell.col)
        if(bottomCell != 0 and bottomCell.color == color):
            self._visitForLink(bottomCell, link)

        rightCell = self.board.getCell(cell.row, cell.col+1)
        if(rightCell != 0 and rightCell.color == color):
            self._visitForLink(rightCell, link)

    def eraseOneLink(self, link, latch):
        """删除一条链上的cell"""
        for i in range(0, len(link)):
            c = link[i]
            self.eraseOneCell(c.row, c.col, latch)

    def eraseOneCell(self, row, col, latch):
        """删除一个格子，并播放动画"""
        cell = self.board.cells[row][col]
        c = latch.createCallback()

        def finished():
            self.board.cells[row][col] = 0
            c()
        cell.blowUp(finished)
    """还有没有cell在动的，如果有，等它完成"""

    def cellMoving(self):
        return cellMoving(self.board.cells)
