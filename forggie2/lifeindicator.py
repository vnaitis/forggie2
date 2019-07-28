"""Life indicator."""
import pygame
from animatedsprite import AnimatedSprite

MAX_LIFES = 10


class LifeIndicator:
    """Class to show life crystal animations."""

    def __init__(self, config, configDir, imageDir):
        """Initialize object to show frog lifes.

        Args:
            config:    Configuration found in game.conf section
                       [LifeIndicator].
                       ConfigParser object.
            configDir: Game settings directory. String.
            imageDir:  Image directory. String.
        """
        self.configDir = configDir
        self.imageDir = imageDir

        font = pygame.font.Font(None, 27)
        self.text = font.render('Lifes:', True, pygame.Color('white'))

        pos = config.get('textPosition').split(',')
        self.textPosition = (int(pos[0]), int(pos[1]))

        self.all = []
        for i in range(1, MAX_LIFES + 1):
            position = config.get('pos' + str(i))
            if position:
                position = position.split(',')
                posX = int(position[0])
                posY = int(position[1])
                self.all.append(AnimatedSprite('life_crystal.conf',
                                               self.configDir, self.imageDir,
                                               (posX, posY), isActive=True))

        self.crystalGroup = pygame.sprite.Group(self.all)

    def resetLifes(self):
        """Set lifes back to maximum."""
        # Make every crystal to show the same animation frame.
        for animation in self.all:
            animation.currentFrame = 0

        self.crystalGroup = pygame.sprite.Group(self.all)

    def update(self, frog):
        """Show how many lifes left on the screen.

        Args:
            frog: Frog object.
        """
        if frog.lifesLeft == 3:
            return

        if frog.lifesLeft == 2:
            self.crystalGroup.remove(self.all[2])

        if frog.lifesLeft == 1:
            self.crystalGroup.remove(self.all[1])

        if frog.lifesLeft == 0:
            self.crystalGroup.remove(self.all[0])

    def draw(self, surface):
        """Draw lifes on the given surface.

        Args:
            surface: Surface to draw on to.
        """
        surface.blit(self.text, self.textPosition)
        self.crystalGroup.update()
        self.crystalGroup.draw(surface)
