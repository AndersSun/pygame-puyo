#!/usr/bin/env python
""" 
puyo
"""


# Import Modules
import os
import pygame as pg
from frameRunner.FrameRunner import FrameRunner
from PuyoAnima import puyoAnima
from GameBoard import GameBoard
from GameBoard import GS_FINISHED, GS_PAUSED
from GameMenu import GameMenu
from PuyoAnima import loadBgImg

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")


class TwoPlayer():
    def __init__(self, screen):
        """ 
        """
        self.screen = screen
        self.command = None
        self.bgImg = loadBgImg()
    def mainLoop(self):
        screen = self.screen
        # Create The Backgound
        background = pg.Surface(screen.get_size())
        background = background.convert()
        background.fill((255,255,255))


        clock = pg.time.Clock()
        board1 = GameBoard(100,0, True)
        board1.restartGame()
        board1.genTestData()

        board2 = GameBoard(650,0, False)
        board2.restartGame()
        board2.genTestData()
        allsprites = pg.sprite.RenderPlain((board1,board2))
        # Main Loop
        while self.command is None:
            clock.tick(60)

            # Handle Input Events
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    board1.pauseGame()
                    board2.pauseGame()
                board1.handleEvent(event)
                board2.handleEvent(event)
                
            allsprites.update()
            background.fill((255,255,255))
            background.blit(self.bgImg, (0,0))
            # Draw Everything
            screen.blit(background, (0, 0))

            allsprites.draw(screen)
            pg.display.flip()
            if board1.gameStatus == GS_FINISHED and board2.gameStatus:
                c = self.showGameOverMenu()
                if c == "restart":
                    board1.restartGame()
                    board1.restartGame()
                else:
                    self.command = c
            elif board1.gameStatus == GS_PAUSED and board2.gameStatus == GS_PAUSED:
                c = self.showPauseMenu()
                if c == "restart":
                    board1.restartGame()
                    board2.restartGame()
                elif c == "resume":
                    board1.resumeGame()
                    board2.resumeGame()
                else:
                    self.command = c

        return self.command
    def showPauseMenu(self):
        """显示暂停菜单"""
        return self.showInnerMenu(True)
    def showGameOverMenu(self):
        """显示游戏结束菜单"""
        return self.showInnerMenu(False)
    def showInnerMenu(self, pauseMenu):
        """显示暂停菜单"""
        pauseCommand = [None]
        def resumeGame():
            pauseCommand[0] = "resume"
        def restart():
            pauseCommand[0] = "restart"
        def mainMenu():
            pauseCommand[0] = "mainMenu"
        if pauseMenu:
            title = "Pause"
        else:
            title = "Game Over"
        theMenu = GameMenu(title, 400, 300)
        if pauseMenu:
            theMenu.addItem('resume game', resumeGame)
        theMenu.addItem('restart', restart)
        theMenu.addItem('main menu', mainMenu)

         # Main Loop
        clock = pg.time.Clock()
        while pauseCommand[0] is None:
            clock.tick(60)

            # Handle Input Events
            events = pg.event.get()
            for event in events:
                if pauseMenu and event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    pauseCommand[0] = "resume"
            # self.screen.fill((250,0,0,0))
           
            theMenu.update(events)
            theMenu.draw(self.screen)
            pg.display.flip()
        return pauseCommand[0]


   
