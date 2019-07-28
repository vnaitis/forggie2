"""Animated sprite."""
import os
import copy
import configparser
import pygame

import loaders

# Amount of frames in animated sprite.
MAX_FRAME_COUNT = 5


class AnimatedSprite(pygame.sprite.Sprite):
    """Class to show animated sprite."""

    def __init__(self, configPath, configDir, imageDir, position, rotate=None,
                 isActive=False):
        """Initialize sprite used to show info data.

        Args:
            configPath:   Relative path to the animation configuration file.
            position:     Tuple with x and y coordinates of the top left
                          corner of the image to be placed on the screen.
            frameRate:    Max frame rate limit for the application.
            rotate:       Angle in degrees to rotate the image. Positive
                          values will rotate counterclockwise, negative -
                          clockwise. Float.
            isActive:     Boolean value that indicates if animation should be
                          running.
            configDir:    Game settings directory. String.
            imageDir:     Image directory. String.
        """
        pygame.sprite.Sprite.__init__(self)

        self.configPath = configPath
        self.configDir = configDir
        self.imageDir = imageDir

        # Load animation configuration.
        config = configparser.ConfigParser()
        config.read(os.path.join(self.configDir, configPath))

        generalCfg = config['general']
        animationCfg = config['animation']
        useAlpha = generalCfg.getboolean('useAlphaChannel', False)

        imageFile = generalCfg['filename']
        imagePath = os.path.join(self.imageDir, imageFile)

        values = animationCfg.get('frameSize').split(',')
        frameWidth = int(values[0])
        frameHeight = int(values[1])

        values = animationCfg.get('collisionFrameSize', '0,0').split(',')
        collWidth = int(values[0])
        collHeight = int(values[1])

        framesConfig = {}
        for i in range(1, MAX_FRAME_COUNT + 1, 1):
            # Get X and Y coordinates of the top left corner of the frame.
            name = 'frame' + str(i)
            try:
                frameXY = animationCfg.get(name).split(',')
                frameTime = animationCfg[name + 'Time']
                dist = animationCfg.get(name + 'MoveDistance')

            except AttributeError:
                continue

            coordX = int(frameXY[0])
            coordY = int(frameXY[1])

            framesConfig[i] = {'frame': (coordX, coordY, frameWidth,
                                         frameHeight),
                               'time': int(frameTime),
                               }

            # Not all animated sprites move, so not all have 'distance'.
            if dist is not None:
                framesConfig[i]['distance'] = int(dist)

        self.loadedImage, self.rect = loaders.loadImage(imagePath,
                                                        useAlpha=useAlpha)
        self.rect.topleft = position

        # Set collision rect to correct position.
        self.horizontalMargin = int((frameWidth - collWidth) / 2)
        self.verticalMargin = int((frameHeight - collHeight) / 2)

        self.collisionRect = pygame.Rect(position[0] + self.horizontalMargin,
                                         position[1] + self.verticalMargin,
                                         collWidth, collHeight)

        self.frames = []
        self.frameTimes = []
        self.distances = []
        for i in range(1, MAX_FRAME_COUNT + 1, 1):
            try:
                config = framesConfig[i]
            except KeyError:
                # We don't know how many frames are present, so it will fail
                # when asked for non-existend frame.
                continue

            # Frame's area inside an image.
            cfg = config['frame']
            area = pygame.Rect(cfg[0], cfg[1], cfg[2], cfg[3])
            value = self.loadedImage.subsurface(area)
            if rotate is not None:
                value = pygame.transform.rotate(value, rotate)

            name = 'image' + str(i)
            setattr(self, name, value)

            self.frames.append(getattr(self, name))
            self.frameTimes.append(config['time'])

            distance = config.get('distance')
            if isinstance(distance, int):
                self.distances.append(distance)

        self.frameCount = len(self.frames)
        self.currentFrame = -1
        self.image = self.frames[self.currentFrame]
        self.currentFrameTime = self.frameTimes[self.currentFrame]

        self.currentFrameStart = pygame.time.get_ticks()

        self.image = self.frames[self.currentFrame]

        # Amount of times to run animation cycle (None - forever).
        self.cycles = None

        # Amount of times animation cycle was done.
        self.cyclesDone = 0

        # Set to True to make animation run.
        self.isActive = isActive

        self.moveDistance = 0

        self.debug = False
        self.currentCycleDistances = copy.copy(self.distances)

    def setPosition(self, position):
        """Set animation's position.

        Args:
            position: Tuple with X and Y coordinates of the point where
                      should be top left corner of the animation.
        """
        self.rect.left = position[0]
        self.rect.top = position[1]

        self.collisionRect.left = self.rect.left + self.horizontalMargin
        self.collisionRect.top = self.rect.top + self.verticalMargin

    def update(self):
        """Change to the next animation frame."""
        if not self.isActive:
            return

        now = pygame.time.get_ticks()
        frameTime = now - self.currentFrameStart

        if frameTime >= self.currentFrameTime:
            self.currentFrame += 1

            if self.currentFrame == self.frameCount - 1:
                self.cyclesDone += 1
                self.currentFrame = -1
                self.currentCycleDistances = copy.copy(self.distances)
                if self.cyclesDone == self.cycles:
                    self.isActive = False

            self.currentFrameStart = pygame.time.get_ticks()
            self.currentFrameTime = self.frameTimes[self.currentFrame]
            self.image = self.frames[self.currentFrame]

            if self.distances:
                self.moveDistance = self.currentCycleDistances[
                    self.currentFrame]
                # We want to move distance once per frame.
                self.currentCycleDistances[self.currentFrame] = 0

    def resetAnimation(self):
        """Reset animation to initial state."""
        self.isActive = False
        self.currentFrame = -1
        self.image = self.frames[self.currentFrame]
        self.currentCycleDistances = copy.copy(self.distances)

    def startAnimation(self, cycles=-1):
        """Fix the start time of the first animation frame.

        Args:
            cycles: Amount of cycles to show the animation. Integer.
                    Use "-1" to cycle forever.
        """
        self.cycles = cycles
        self.cyclesDone = 0
        self.isActive = True
        self.currentFrameStart = pygame.time.get_ticks()
