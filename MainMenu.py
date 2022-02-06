#!/usr/bin/env python
import pygame as pg

from GameMenu import GameMenu
from PuyoAnima import load_image
from Contants import *
from PuyoAnima import loadBgImg
""" 
puyo
"""
class MainMenu:
    def __init__(self, screen):
        """ 
        """
        self.screen = screen
        self.command = None
        def onePlayer():
                self.command = "singlePlayer"
        def twoPlayer():
            self.command = "twoPlayer"
        def quit():
            self.command = "quit"
        self.menu = GameMenu('Welcome', 400, 300)
        
        self.menu.addItem('Single Player', onePlayer)
        self.menu.addItem('Two Player', twoPlayer)
        self.menu.addItem('Quit', quit)

        self.bgImg = loadBgImg()
        
    def mainLoop(self):

        # Main Loop
        clock = pg.time.Clock()
        while self.command is None:
            clock.tick(60)

            # Handle Input Events
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.command = "quit"
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.command = "quit"
            self.screen.fill((255,255,255))
            self.screen.blit(self.bgImg, (0,0))
            
            self.menu.update(events)
            self.menu.draw(self.screen)
            pg.display.flip()
        return self.command
