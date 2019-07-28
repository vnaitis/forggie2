""""Class to load a level."""
import os
import configparser

import pygame

from staticsprite import StaticImage
from frog import Frog
from car import Car
from floater import Floater


class Level:
    """Holds level parameters as attributes."""

    def __init__(self, configDir, imageDir, screenWidth, screenHeight):
        """Initialize level.

        Args:
            configDir:   Absolute path to the configuration folder. String.
            imageDir:    Absolute path to the image folder. String.
            screenWidth: Game window width in pixels. Integer.
            screenHeight Game window height in pixels. Integer.
        """
        self.configDir = configDir
        self.imageDir = imageDir
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        # Car track section configuration names from level?.conf files.
        self.allowedTrackSections = ('track1', 'track2', 'track3', 'track4',
                                     'track5')

        # Water object track section configuration names in level?.conf files.
        self.allowedRiverSections = ('waterTrack1', 'waterTrack2',
                                     'waterTrack3', 'waterTrack4',
                                     'waterTrack5')

        # Level Name. String.
        self.name = None

        # Level background image.
        self.background = None

        # Starting position of the frog. Integers.
        self.frogPosX = None
        self.frogPosY = None

        # Frog collision rect is a little bit smaller than image rect. These
        # numbers define collision rect's width and height. Integers.
        self.frogCollisionWidth = None
        self.frogCollisionHeight = None

        # Frog object.
        self.frog = None

        # Finish image.
        self.finishImage = None

        # List of car objects used in the level.
        self.cars = None

        # List of dictionaries defining each water track.
        self.riverTracks = None

        # List of river tracks' rects to use later for collision detection.
        self.riverTrackRects = None

        # List of floater objects used in the level.
        self.floaters = None

        # List of StaticImage's of car shadows.
        self.shadows = None

    def loadCars(self, config, allowedSections):
        """Load all cars used in the level.

        Args:
            config:          Parsed level config object.
                             configparser.ConfigParser object.
            allowedSections: List or tuple of names used in configuration
                             files to specify configuration for a track
                             section.
        """
        cars = []
        shadows = []
        for trackSection in allowedSections:
            print(f'Loading track: {trackSection}')

            if not config[trackSection].getboolean('enabled'):
                continue

            cfg = config[trackSection]

            gaps = []
            for amount in cfg.get('gaps').replace(' ', '').split(','):
                gaps.append(int(amount))

            track = {'top': cfg.getint('top'),
                     'bottom': cfg.getint('bottom'),
                     'direction': cfg.get('direction'),
                     'speed': cfg.getint('speed'),
                     'gaps': gaps,
                     }

            # Get names of config files for cars for the level.
            configFilenames = cfg.get('cars').replace(' ', '').split(',')

            # Load specified cars.
            trackCars = []
            carShadows = []
            carWidth = 0
            initPos = 0
            for idx, configName in enumerate(configFilenames):
                configPath = os.path.join(self.configDir, configName)
                if idx == len(gaps):
                    msg = (f"No gap defined for car '{configPath}' in "
                           f"section '{trackSection}'.")
                    print(msg)
                    raise ValueError(msg)
                car = Car(configPath, roadDirection=track['direction'],
                          screenWidth=self.screenWidth,
                          screenHeight=self.screenHeight,
                          roadTop=track['top'], roadBottom=track['bottom'],
                          gapInFront=gaps[idx], speed=track['speed'])

                # Calculate and set starting position of the car.
                if idx == 0:
                    carWidth = car.carWidth

                    if car.direction == 'to_left':
                        initPos = car.initPos = car.gap
                    else:
                        initPos = car.initPos = self.screenWidth - car.gap

                    car.gap = 0
                    car.calcPositions()

                else:
                    if car.direction == 'to_left':
                        car.initPos = initPos + carWidth + car.gap
                    else:
                        car.initPos = initPos - car.carWidth - car.gap
                    car.calcPositions()

                    initPos = car.initPos
                    carWidth = car.carWidth

                trackCars.append(car)
                carShadows.append(car.shadow)

            cars += trackCars
            shadows += carShadows

        return (cars, shadows)

    def loadFloaters(self, config, allowedSections):
        """Load objects floating in the water.

        Args:
            config:          Parsed level config object.
                             configparser.ConfigParser object.
            allowedSections: List or tuple of names used in configuration
                             files to specify configuration for a track
                             section.
        """
        riverTracks = []
        floatingObjects = []
        for trackSection in allowedSections:

            if not config[trackSection].getboolean('enabled'):
                continue

            cfg = config[trackSection]

            gaps = []
            for amount in cfg.get('gaps').replace(' ', '').split(','):
                gaps.append(int(amount))

            track = {'top': cfg.getint('top'),
                     'bottom': cfg.getint('bottom'),
                     'direction': cfg.get('direction'),
                     'speed': cfg.getint('speed'),
                     'gaps': gaps,
                     }
            riverTracks.append(track)

            # Get names of config files for the floaters for the level.
            configFilenames = cfg.get('floaters').replace(' ', '').split(',')

            # Load specified water objects.
            waterObjects = []
            for idx, configName in enumerate(configFilenames):
                configPath = os.path.join(self.configDir, configName)
                if idx == len(gaps):
                    msg = (f"No gap defined for floater '{configPath}' in "
                           f"section '{trackSection}'.")
                    print(msg)
                    raise ValueError(msg)
                stuff = Floater(configPath,
                                roadDirection=track['direction'],
                                screenWidth=self.screenWidth,
                                screenHeight=self.screenHeight,
                                roadTop=track['top'],
                                roadBottom=track['bottom'],
                                gapInFront=gaps[idx],
                                speed=track['speed'])

                # Calculate and set starting position of the floater.
                if idx == 0:
                    carWidth = stuff.carWidth

                    if stuff.direction == 'to_left':
                        initPos = stuff.initPos = stuff.gap
                    else:
                        initPos = stuff.initPos = self.screenWidth - stuff.gap

                    stuff.gap = 0
                    stuff.calcPositions()

                else:
                    if stuff.direction == 'to_left':
                        stuff.initPos = initPos + carWidth + stuff.gap
                    else:
                        stuff.initPos = initPos - stuff.carWidth - stuff.gap
                    stuff.calcPositions()

                    initPos = stuff.initPos
                    carWidth = stuff.carWidth

                waterObjects.append(stuff)

            floatingObjects += waterObjects

        return (riverTracks, floatingObjects)

    def load(self, levelConfigPath):
        """Load the level.

        Args:
            levelConfigPath: Absolute path to the level configuration
                             file. String.
        """
        config = configparser.ConfigParser()
        config.read(levelConfigPath)

        cfg = config['general']
        self.name = cfg.get('name', '')

        # Level background image.
        path = cfg.get('background')
        self.background = StaticImage(os.path.join(self.imageDir, path))

        self.frogPosX = cfg.getint('frogPosX')
        self.frogPosY = cfg.getint('frogPosY')
        self.frogCollisionWidth = cfg.getint('frogCollisionWidth')
        self.frogCollisionHeight = cfg.getint('frogCollisionHeight')

        path = cfg.get('frog')
        self.frog = Frog(self.frogPosX, self.frogPosY,
                         self.screenWidth, self.screenHeight,
                         self.configDir, self.imageDir)

        # Load finish image.
        filepath = cfg.get('finishImage')
        posX = cfg.getint('finishImageX')
        posY = cfg.getint('finishImageY')
        centerX = cfg.getint('finishCenterWidth')
        centerY = cfg.getint('finishcenterHeight')

        finish = StaticImage(os.path.join(self.imageDir, filepath),
                             useAlpha=True)
        finish.rect.topleft = (posX, posY)
        width = int((finish.rect.width - centerX) / 2)
        height = int((finish.rect.height - centerY) / 2)
        finish.collisionRect = pygame.Rect(finish.rect.left + width,
                                           finish.rect.top + height,
                                           centerX, centerY)
        self.finishImage = finish

        self.cars, self.shadows = self.loadCars(config,
                                                self.allowedTrackSections)

        riverTracks, floatingObjects = self.loadFloaters(
            config, self.allowedRiverSections)

        if riverTracks:
            riverTrackRects = []
            for track in riverTracks:
                rect = pygame.Rect(0, track['top'], self.screenWidth,
                                   track['bottom'] - track['top'])
                riverTrackRects.append(rect)

        self.riverTracks = riverTracks
        self.floaters = floatingObjects
        self.riverTrackRects = riverTrackRects
