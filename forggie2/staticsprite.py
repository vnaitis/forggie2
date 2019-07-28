"""Slightly extended sprite class."""
import copy
import pygame
import loaders


class StaticImage(pygame.sprite.Sprite):
    """Class to show simple, non-animated sprite"""

    def __init__(self, imagePath, useAlpha=True):
        """Initialize.

        Args:
            imagePath: Relative path to the image. String.
            useAlpha:  Use image's alpha channel for transparency
                       data. Boolean.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = loaders.loadImage(imagePath, useAlpha=useAlpha)
        self.collisionRect = copy.deepcopy(self.rect)
