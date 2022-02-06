#!/usr/bin/env python
"""
puyo
"""

# pip install pygame-menu -U
# Import Modules
import os
import pygame as pg
from frameRunner.FrameRunner import FrameRunner
from PuyoAnima import puyoAnima
from GameBoard import GameBoard
from MainMenu import MainMenu
from SinglePlayer import SinglPlayer
from TwoPlayer import TwoPlayer
from Contants import *

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

def createMainMenuWin(screen):
    return MainMenu(screen)
def createSinglePlayerWin(screen):
    return SinglPlayer(screen)
def createTwoPlayerWin(screen):
    return TwoPlayer(screen)

windows = {
    "mainMenu": createMainMenuWin,
    "singlePlayer": createSinglePlayerWin,
    "twoPlayer": createTwoPlayerWin,
}



def main():
    """this function is called when the program starts.
    it initializes everything it needs, then runs in
    a loop until the function returns."""
    # Initialize Everything
    pg.init()
    puyoAnima.init()
    screen = pg.display.set_mode((screenWidth, screenHeight), pg.SCALED)
    pg.display.set_caption("puyo")
    pg.mouse.set_visible(False)

    currentWin = "mainMenu"
    # Main Loop
    going = True
    while going:
        if(currentWin == "quit"):
            going = False
            break
        windowCreator = windows[currentWin]
        win = windowCreator(screen)
        currentWin = win.mainLoop()

    pg.quit()


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()
