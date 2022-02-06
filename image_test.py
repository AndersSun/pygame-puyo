#!/usr/bin/env python
""" 
runner test
"""


# Import Modules
import pygame as pg

from frameRunner.FrameRunner import FrameRunner
from Animation import createBySheet
from PuyoAnima import puyoAnima

width = 1800
height = 1000



def main():
    # Initialize Everything
    pg.init()

    screen = pg.display.set_mode((width, height), pg.SCALED)
    pg.display.set_caption("image test")

    bgcolor = (0, 0, 0, 0)
    # Create The Backgound
    background = pg.Surface((500,500))
    background = background.convert_alpha()
    # background.set_colorkey(bgcolor)
    puyoAnima.init()
    img = puyoAnima.redInPieceFrames[0][0]
    

    clock = pg.time.Clock()
    # Main Loop
    going = True
    while going:
        clock.tick(1)

        # Handle Input Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False

        background.fill(bgcolor)
        background.blit(img, (0, 0))

        # Display The Background
        screen.fill((255, 0, 0))
        screen.blit(background, (0, 0))

        pos = (0,0)
        color1 = img.get_at(pos)
        color2 = background.get_at(pos)
        pg.display.flip()

    pg.quit()


# Game Over


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()
