
from pygame import KEYDOWN, K_w, Rect, Surface
import pygame as pg
from pygame import *


class MenuItemEntry():
    def __init__(self, font, itemText, handler):
        pass
        self.itemText = itemText
        self.handler = handler
        self.itemSurface = font.render(itemText, True, (255, 255, 0))

        self.rect = None


class GameMenu():
    """game menu """

    def __init__(self, title, width, height):
        """ 
        """
        self.itemFont = pg.font.Font(None, 50)
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width, self.height)).convert_alpha()
        self.items = []
        self.padding = 10
        self.upKeys = [K_UP, K_w]
        self.downKeys = [K_DOWN, K_s]
        self.confirmKeys = [K_RETURN, K_d, K_RIGHT]
        self.activeItem = 0

    def draw(self, surface: Surface):
        """pass """
        parentRect: Rect = surface.get_rect()
        offectX = (parentRect.width - self.width)/2
        offectY = (parentRect.height - self.height)/2
        self.rect = (parentRect.left+offectX, parentRect.top +
                     offectY, self.width, self.height)
        self.image.fill((100, 0, 0,100))
        self._drawItems(self.image, (20, 20))
        surface.blit(self.image, self.rect)

    def _drawItems(self, menuSurface: Surface, pos):
        x, y = pos
        for i in range(0, len(self.items)):
            item = self.items[i]
            itemSurface = item.itemSurface
            menuSurface.blit(itemSurface, (x, y))

            size = itemSurface.get_size()
            item.rect = (x, y, size[0], size[1])
            if i == self.activeItem:
                pg.draw.rect(menuSurface, (0, 255, 255), item.rect, 1)
            y += size[1]+self.padding

    def addItem(self, itemText, handler):
        """pass """
        entry: MenuItemEntry = MenuItemEntry(self.itemFont, itemText, handler)
        self.items.append(entry)

    def update(self, events):
        for event in events:
            if(event.type == KEYDOWN):
                if event.key in self.upKeys:
                    if(self.activeItem > 0):
                        self.activeItem -= 1
                elif event.key in self.downKeys:
                    if(self.activeItem < len(self.items)-1):
                        self.activeItem += 1
                elif event.key in self.confirmKeys:
                    self.items[self.activeItem].handler()
