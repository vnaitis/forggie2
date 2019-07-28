"""Functions to load data (images, sounds etc.)."""

import os
import pygame
from pygame.locals import *

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
IMAGES_DIR = os.path.join(MAIN_DIR, '..', 'images')

# No sounds in game at the moment.
SOUNDS_DIR = os.path.join(MAIN_DIR, '..', 'sounds')


def loadImage(name, useAlpha=False):
    """Load image.

    Args:
        name:     Image filename. String.
        useAlpha: Should we use image's alpha channel and there defined
                  transparency? Boolean.
    """
    fullname = os.path.join(IMAGES_DIR, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print(f'Could not load image: {fullname}')
        raise SystemExit(str(geterror()))

    method = ''
    if useAlpha:
        method = 'alpha channel'
        image.convert_alpha()

    else:
        image.convert()

    print(f'Successfully loaded {fullname}.')

    return image, image.get_rect()


def loadSound(name):
    """Load sound."""
    fullname = os.path.join(SOUNDS_DIR, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print(f'Could not load sound file: {fullname}')
        raise SystemExit(str(geterror()))

    return sound
