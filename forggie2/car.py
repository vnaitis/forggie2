"""Class defining car on the street."""
import random
import configparser

import pygame

import loaders
from staticsprite import StaticImage


class Car(pygame.sprite.Sprite):
    """Traffic car."""

    def __init__(self, configPath, roadDirection, screenWidth=0,
                 screenHeight=0, roadTop=0, roadBottom=0, gapInFront=0,
                 speed=0):
        """Initialize car object.

        Args:
            configPath:    Path to the configuration file.
            roadDirection: Direction in which all cars on the road should move.
                           'to_left' or 'to_right'.
            screenWidth:   Screen width in pixels. Integer.
            screenHeight:  Screen height in pixels. Integer.
            roadTop:       Y coordinate of the track top. Integer.
            roadBottom:    Y coordinate of the track bottom. Integer.
            gapInFront:    Integer which specifies how many pixels to leave
                           in front of the car.
            speed:         Speed at which car is moving. Integer.
        """
        pygame.sprite.Sprite.__init__(self)

        self.configPath = configPath
        config = configparser.ConfigParser()
        config.read(configPath)

        # Load car image.
        path = config['general']['image']
        self.image, self.rect = loaders.loadImage(path, useAlpha=True)

        # Load car shadow.
        path = config['general']['shadow_image']
        self.shadow = StaticImage(path, useAlpha=True)

        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.roadTop = roadTop
        self.roadBottom = roadBottom


        # Amount of pixels from the border towards which car is moving.
        self.initPos = 0

        # Gap between current car's front and the back of the car in front.
        self.gap = gapInFront # + random.randint(-15, 15)

        self.speed = speed

        self.direction = roadDirection
        carDirection = config['general']['direction']
        if roadDirection != carDirection:
            self.image = pygame.transform.rotate(self.image, 180)

        self.carWidth = self.rect.width

        cfg = config['general']
        self.crMarginTop = cfg.getint('crMarginTop')
        self.crMarginBottom = cfg.getint('crMarginBottom')
        self.crMarginLeft = cfg.getint('crMarginLeft')
        self.crMarginRight = cfg.getint('crMarginRight')
        self.collisionRect = pygame.Rect(
            self.rect.left + self.crMarginLeft,
            self.rect.top + self.crMarginTop,
            self.rect.width - self.crMarginRight,
            self.rect.height - self.crMarginBottom)

        # Space between car and top of the track.
        self.freeVerticalSpace = (self.roadBottom
                                  - self.roadTop
                                  - self.rect.height)

    def __unicode__(self):
        msg = (f'Car(configPath={self.configPath}, '
               f'roadDirection={self.direction}, '
               f'screenWidth={self.screenWidth}, '
               f'screenHeight={self.screenHeight}, '
               f'roadTop={self.roadTop}, '
               f'roadBottom={self.roadBottom}, '
               f'gapInFront={self.gap}, '
               f'speed={self.speed})')
        return msg

    def __str__(self):
        return self.__unicode__()

    def calcPositions(self):
        """Calculate initial positions of car's sprites."""
        self.roadTopGap = random.randint(2, self.freeVerticalSpace)

        # Place car on the road.
        if self.direction == 'to_left':
            self.rect.topleft = (self.initPos, self.roadTop + self.roadTopGap)
            self.speed *= -1

        else:
            self.rect.topleft = (self.initPos, self.roadTop + self.roadTopGap)

        self.collisionRect.topleft = (self.rect.top + self.crMarginTop,
                                      self.rect.left + self.crMarginLeft)

        self.shadow.rect.topleft = (self.rect.left, self.rect.top - 4)

    def update(self):
        """Move car."""
        self.rect.move_ip(self.speed, 0)

        # If car leaves the screen, move to the opposite side of the screen.
        if self.direction == 'to_left':
            # If car is enough outside of the screen, move it back to the
            # other side of the screen.
            # '-80' - number a little bit higher that the longest car.
            # Moving cars to the other side of the screen as soon as they hit
            # specific coordinate makes it significantly simplier to keep
            # distances between them consistent when lengths of cars differ.
            if self.rect.topleft[0] <= -80:
                # Keeps distance between first appearance on the screen after
                # moving to the other side of the screen.
                tmp = -80 - self.rect.topleft[0]
                self.rect.topleft = (20 - tmp + self.screenWidth,
                                     self.roadTop + self.roadTopGap)

        else:
            if self.rect.bottomright[0] >= self.screenWidth + 80:
                tmp = self.screenWidth + 80 - self.rect.bottomright[0]
                # If car is already outside the screen, move it back to the
                # other side of the screen.
                self.rect.topleft = (-20 - self.carWidth - tmp,
                                     self.roadTop + self.roadTopGap)
                self.roadTopGap = random.randint(2, self.freeVerticalSpace)

        self.collisionRect.topleft = (self.rect.left + self.crMarginLeft,
                                      self.rect.top + self.crMarginTop)

        self.shadow.rect.topleft = (self.rect.left, self.rect.top - 4)
