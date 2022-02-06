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

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")


def drawGrid(surface):
    for row in range(0, 15):
        y = row * 72 - 4
        pg.draw.line(surface, (255, 255, 0), (0, y), (width, y), 1)
    for col in range(0, 17):
        x = col * 72 - 4
        pg.draw.line(surface, (255, 255, 0), (x, 0), (x, height), 1)




def main():
    # Initialize Everything
    pg.init()

    screen = pg.display.set_mode((width, height), pg.SCALED)
    pg.display.set_caption("runner test")

    # Create The Backgound
    background = pg.Surface(screen.get_size())
    background = background.convert()
    puyoAnima.init()
    img = puyoAnima.img
    background.fill((0, 0, 0))
    background.blit(img, (0, 0))
    drawGrid(background)

    # Display The Background
    screen.blit(background, (0, 0))
    pg.display.flip()

    clock = pg.time.Clock()
    fr = FrameRunner()
    
    animation = puyoAnima.createPurpleBlowUp(fr)

    # Main Loop
    going = True
    while going:
        clock.tick(60)

        # Handle Input Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
        fr.update()

        screen.fill((255, 0, 0))
        # Draw Everything
        screen.blit(background, (0, 0))
        animation.blit(screen, (1200, 505))
        pg.display.flip()

    pg.quit()


# Game Over


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()
