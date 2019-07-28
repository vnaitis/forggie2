"""Class defining main character."""
import os
import configparser
import pygame
from animatedsprite import AnimatedSprite


class Frog:
    """Animated frog."""

    def __init__(self, startX, startY, screenWidth, screenHeight,
                 configDir, imageDir):
        """Initialize main character object.

        Args:
            startX:       X coordinate of the initial frog position.
                          Integer.
            startY:       Y coordinate of the initial frog position.
                          Integer.
            screenWidth:  Game screen width. Integer
            screenHeight: Game screen heigh. Integer.
            frameRate:    Frame rate for animations.
            configDir:    Game settings directory. String.
            imageDir:     Image directory. String.
        """
        self.configDir = configDir
        self.imageDir = imageDir
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self.pressedUp = False
        self.pressedDown = False
        self.pressedLeft = False
        self.pressedRight = False

        # Initial frog position.
        self.position = (startX, startY)
        self.startPosition = self.position

        # Frog animation to jump up.
        self.jumpUpAnim = AnimatedSprite('animation_frog_up.conf',
                                         self.configDir, self.imageDir,
                                         self.position)

        # Frog animation to move left when facing up.
        self.jumpUpLeftAnim = AnimatedSprite('animation_frog_left.conf',
                                             self.configDir, self.imageDir,
                                             self.position)

        # Frog animation to move right when facing up.
        self.jumpUpRightAnim = AnimatedSprite('animation_frog_right.conf',
                                              self.configDir, self.imageDir,
                                              self.position)

        # Frog animation to jump down.
        #self.jumpDownAnim = AnimatedSprite('animation_frog_up.conf',
        self.jumpDownAnim = AnimatedSprite('animation_frog_down.conf',
                                           self.configDir, self.imageDir,
                                           self.position)

        # Frog animation to move left when facing down.
        self.jumpDownLeftAnim = AnimatedSprite('animation_frog_down_left.conf',
                                               self.configDir, self.imageDir,
                                               self.position)

        # Frog animation to move rigt when facing down.
        self.jumpDownRightAnim = AnimatedSprite('animation_frog_down_right.conf',
                                                self.configDir, self.imageDir,
                                                self.position)

        # Initial frog position.
        self.anim = self.jumpUpAnim

        # All sprites to animate at the same time for the frog.
        self.all = pygame.sprite.Group(self.jumpUpAnim)

        # Every sprite can only be moved in 4 directions in 2D space. This
        # attribute tells us, which animation is currently running: 'up',
        # 'down', 'left', 'right' and None.
        self.activeAnimation = 'up'

        # Is frog facing up? Required to know which animation to show when
        # animating stepping sideways.
        self.isFacingUp = True

        self.collisionRect = self.anim.collisionRect

        # Image to show frog after being run over by a car.
        self.deadFrog = AnimatedSprite('animation_dead.conf', self.configDir,
                                       self.imageDir, self.position)

        # Image to show when frog drawned in the river.
        self.drownedFrog = AnimatedSprite('animation_drowning.conf',
                                          self.configDir, self.imageDir,
                                          self.position)
        self.drownedFrog.cycles = 1

        # Was frog run over by a car?
        self.isDead = False

        # Has frog drowned?
        self.isDrowned = False

        # Frog is not dead, but should not move. Used to wait until user
        # presses <enter> to load next level.
        self.isLocked = False

        # Amount of lifes frog has.
        self.lifesLeft = 3

        # Boolean to mark that ran over frog image is being shown.
        self.showingDeadFrog = False

        # Boolean to mark that drowned frog image is being shown.
        self.showingDrownedFrog = False

        self.runningDrowningAnim = False

        # Debug option.
        self.drawCollisionRects = False

    # covered with tests
    def moveUp(self):
        """Move sprite vertically up on the screen."""
        newX = self.anim.collisionRect.top - self.anim.moveDistance

        if newX <= 0:
            dist = -self.anim.moveDistance - newX
            self.anim.rect.move_ip(0, dist)
            self.anim.collisionRect.move_ip(0, dist)

        else:
            self.anim.rect.move_ip(0, -self.anim.moveDistance)
            self.anim.collisionRect.move_ip(0, -self.anim.moveDistance)

    # covered with tests
    def moveDown(self):
        """Move sprite vertically down on the screen."""
        newX = self.anim.collisionRect.bottom + self.anim.moveDistance

        if newX >= self.screenHeight:
            dist = self.anim.moveDistance - (newX - self.screenHeight)
            self.anim.rect.move_ip(0, dist)
            self.anim.collisionRect.move_ip(0, dist)

        else:
            self.anim.rect.move_ip(0, self.anim.moveDistance)
            self.anim.collisionRect.move_ip(0, self.anim.moveDistance)

    # covered with tests
    def moveLeft(self):
        """Move sprite horizontally to the left."""
        newY = self.anim.collisionRect.left - self.anim.moveDistance

        if newY <= 0:
            dist = -self.anim.moveDistance - newY
            self.anim.rect.move_ip(dist, 0)
            self.anim.collisionRect.move_ip(dist, 0)

        else:
            self.anim.rect.move_ip(-self.anim.moveDistance, 0)
            self.anim.collisionRect.move_ip(-self.anim.moveDistance, 0)

    # covered with tests
    def moveRight(self):
        """Move sprite horizontally to the right."""
        newY = self.anim.collisionRect.right + self.anim.moveDistance

        if newY >= self.screenWidth:
            dist = self.anim.moveDistance - (newY - self.screenWidth)
            self.anim.rect.move_ip(dist, 0)
            self.anim.collisionRect.move_ip(dist, 0)

        else:
            self.anim.rect.move_ip(self.anim.moveDistance, 0)
            self.anim.collisionRect.move_ip(self.anim.moveDistance, 0)

    def moveToStart(self):
        """Move frog to the initial starting position."""
        self.anim = self.jumpUpAnim
        self.anim.setPosition(self.startPosition)
        self.collisionRect.center = self.anim.collisionRect.center
        self.activeAnimation = 'up'
        self.isFacingUp = True

        # Reset animation to start position.
        self.anim.resetAnimation()

        # Add animation to the group, so it is displayed.
        self.all.empty()
        self.all.add(self.anim)

    # covered with tests
    def move(self, speed):
        """Move frog automatically when background moves.

        Args:
            speed: Amount of pixels to move the frog. Integer.
        """
        if speed <= 0:
            newY = self.anim.rect.left + speed
            if newY <= 0:
                dist = speed - newY
                self.anim.rect.move_ip(dist, 0)
                self.anim.collisionRect.move_ip(dist, 0)
            else:
                self.anim.rect.move_ip(speed, 0)
                self.anim.collisionRect.move_ip(speed, 0)

        else:
            newY = self.anim.rect.right + speed
            if newY >= self.screenWidth:
                dist = speed - (newY - self.screenWidth)
                self.anim.rect.move_ip(dist, 0)
                self.anim.collisionRect.move_ip(dist, 0)
            else:
                self.anim.rect.move_ip(speed, 0)
                self.anim.collisionRect.move_ip(speed, 0)

    def update(self, hitByCars, inRiver, onFloater, floaters, riverTracks):
        """Update frog animation.

        Args:
            hitByCars:   List of cars by which frog is run over.
            inRiver:     Integer. -1 - not in river, positive - river
                         track index.
            onFloater:   Integer. -1 - frog is not on a floater. Any
                         other value is id of the object on which
                         stands frog.
            floaters:    All Floater objects.
            riverTracks: River track configuration dictionary.
        """
        if hitByCars != -1 and not self.isDead:
            self.isDead = True
            self.lifesLeft -= 1

            # Display dead frog sprite.
            self.showingDeadFrog = True

            self.deadFrog.rect.topleft = self.anim.rect.topleft
            self.deadFrog.collisionRect.center = self.anim.collisionRect.center
            self.anim = self.deadFrog
            self.all.empty()
            self.all.add(self.anim)

        if (inRiver != -1 and onFloater == -1
                and not self.isDrowned):
            self.isDrowned = True
            self.runningDrowningAnim = False
            self.lifesLeft -= 1

            # Display drowned frog sprite.
            self.showingDrownedFrog = True

            self.drownedFrog.rect.topleft = self.anim.rect.topleft
            self.drownedFrog.collisionRect.center = \
                self.anim.collisionRect.center
            self.anim = self.drownedFrog
            self.all.empty()
            self.all.add(self.anim)

        # Frog has to move with floater when on top of it.
        if onFloater != -1:
            speed = floaters[onFloater].speed
            self.move(speed)
            self.collisionRect.center = self.anim.collisionRect.center

        # If in river, but not on a floater.
        if inRiver != -1 and onFloater == -1:
            speed = riverTracks[inRiver]['speed']
            if riverTracks[inRiver]['direction'] == 'to_left':
                speed = -speed

            self.move(speed)
            self.collisionRect.center = self.anim.collisionRect.center

        if self.isDead or self.isDrowned or self.isLocked:
            self.pressedUp = False
            self.pressedDown = False
            self.pressedLeft = False
            self.pressedRight = False

        isAnimationRunning = self.anim.isActive

        if not isAnimationRunning:
            startAnimation = False

            if self.isDrowned and not self.runningDrowningAnim:
                self.runningDrowningAnim = True
                startAnimation = True

            if self.pressedUp:
                self.activeAnimation = 'up'
                self.isFacingUp = True

                tmp = self.anim.rect.topleft
                tmpColl = self.anim.collisionRect.center
                self.anim = self.jumpUpAnim
                self.anim.rect.topleft = tmp
                self.anim.collisionRect.center = tmpColl
                startAnimation = True

            elif self.pressedDown:
                self.activeAnimation = 'down'
                self.isFacingUp = False

                tmp = self.anim.rect.topleft
                tmpColl = self.anim.collisionRect.center
                self.anim = self.jumpDownAnim
                self.anim.rect.topleft = tmp
                self.anim.collisionRect.center = tmpColl
                startAnimation = True

            elif self.pressedLeft:
                self.activeAnimation = 'left'
                tmp = self.anim.rect.topleft
                tmpColl = self.anim.collisionRect.center

                if self.isFacingUp:
                    self.anim = self.jumpUpLeftAnim
                else:
                    self.anim = self.jumpDownLeftAnim

                self.anim.rect.topleft = tmp
                self.anim.collisionRect.center = tmpColl
                startAnimation = True

            elif self.pressedRight:
                self.activeAnimation = 'right'

                tmp = self.anim.rect.topleft
                tmpColl = self.anim.collisionRect.center

                if self.isFacingUp:
                    self.anim = self.jumpUpRightAnim
                else:
                    self.anim = self.jumpDownRightAnim

                self.anim.rect.topleft = tmp
                self.anim.collisionRect.center = tmpColl
                startAnimation = True

            if startAnimation:
                isAnimationRunning = True
                if not self.anim.isActive:
                    self.all.empty()

                self.anim.startAnimation(cycles=1)
                self.all.add(self.anim)

        # We disable movement buttons while frog animation is playing.
        self.pressedUp = False
        self.pressedDown = False
        self.pressedLeft = False
        self.pressedRight = False

        if isAnimationRunning:
            if self.activeAnimation == 'up':
                self.moveUp()

            elif self.activeAnimation == 'down':
                self.moveDown()

            elif self.activeAnimation == 'left':
                self.moveLeft()

            elif self.activeAnimation == 'right':
                self.moveRight()

        self.collisionRect.center = self.anim.collisionRect.center
        self.all.update()

    def draw(self, surface):
        """Draw frogs image or animation frame.

        Args:
            surface: Surface to draw sprites on to.
        """
        if self.drawCollisionRects:
            pygame.draw.rect(surface, (0, 255, 0), self.anim.collisionRect, 1)
            pygame.draw.rect(surface, (255, 0, 0), self.collisionRect, 1)

        self.all.draw(surface)
