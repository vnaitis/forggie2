"""Class defining object floating in the river."""
import configparser
import pygame
import loaders


class Floater(pygame.sprite.Sprite):
    """A thing that floats on water."""

    def __init__(self, configPath, roadDirection, screenWidth=0,
                 screenHeight=0, roadTop=0, roadBottom=0, gapInFront=0,
                 speed=0):
        """
        Args:
            configPath:    Path to the configuration file.
            roadDirection: Direction in which all cars on the road
                           should move.  'to_left' or 'to_right'.
            screenWidth:   Screen width in pixels. Integer.
            screenHeight:  Screen height in pixels. Integer.
            roadTop:       Y coordinate of the track top. Integer.
            roadBottom:    Y coordinate of the track bottom. Integer.
            gapInFront:    Integer which specifies how many pixels to
                           leave in front of the car.
            speed:         Speed at which car is moving. Integer.
        """
        pygame.sprite.Sprite.__init__(self)

        config = configparser.ConfigParser()
        config.read(configPath)

        imageFilename = config['general']['image']
        self.image, self.rect = loaders.loadImage(imageFilename, useAlpha=True)

        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.roadTop = roadTop
        self.roadBottom = roadBottom

        # Amount of pixels from the border towards which the floater is moving.
        self.initPos = 0

        # Gap between current floater's front and the back of the floater
        # in front.
        self.gap = gapInFront

        self.speed = speed

        self.direction = roadDirection
        if roadDirection != config['general']['direction']:
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
        self.roadTopGap = int(self.freeVerticalSpace / 2)

        self.collisionRect.topleft = (self.rect.top + self.crMarginTop,
                                      self.rect.left + self.crMarginLeft)

    def calcPositions(self):
        """Calculate initial positions of floater's sprites."""

        # Place floater on the road.
        if self.direction == 'to_left':
            self.rect.topleft = (self.initPos, self.roadTop + self.roadTopGap)
            self.speed *= -1

        else:
            self.rect.topleft = (self.initPos, self.roadTop + self.roadTopGap)

        self.collisionRect.topleft = (self.rect.top + self.crMarginTop,
                                      self.rect.left + self.crMarginLeft)

    def update(self):
        """Move car."""
        self.rect.move_ip(self.speed, 0)

        # If car leaves the screen, make it start driving again.
        if self.direction == 'to_left':
            if self.rect.bottomright[0] < 0:
                self.rect.topleft = (self.screenWidth,
                                     self.roadTop + self.roadTopGap)

        else:
            if self.rect.bottomleft[0] > self.screenWidth:
                self.rect.topleft = (-self.carWidth,
                                     self.roadTop + self.roadTopGap)

        self.collisionRect.topleft = (self.rect.left + self.crMarginLeft,
                                      self.rect.top + self.crMarginTop)
