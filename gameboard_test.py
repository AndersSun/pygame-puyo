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

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")




def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(data_dir, name)
    sound = pg.mixer.Sound(fullname)

    return sound



def main():
    """this function is called when the program starts.
    it initializes everything it needs, then runs in
    a loop until the function returns."""
    # Initialize Everything
    pg.init()
    puyoAnima.init()
    screen = pg.display.set_mode((1280,900), pg.SCALED)
    pg.display.set_caption("puyo")
    pg.mouse.set_visible(False)

    # Create The Backgound
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((255,255,255))


    clock = pg.time.Clock()
    board = GameBoard(100,50, True)
    board.restartGame()
    board.genTestData()
    allsprites = pg.sprite.RenderPlain((board))
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
            board.handleEvent(event)
        allsprites.update()
        screen.fill((250,0,0))
        # Draw Everything
        screen.blit(background, (0, 0))

        allsprites.draw(screen)
        

        pg.display.flip()

    pg.quit()


# Game Over


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()
