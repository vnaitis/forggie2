#!/usr/bin/env python
"""Forggie. Try 2."""

import os
import sys
import bisect
import functools
import configparser

import pygame
from pygame.locals import *

from level import Level
from logger import Logger
from highscores import Highscores
from staticsprite import StaticImage
from lifeindicator import LifeIndicator

if not pygame.font:
    print('Warning, fonts disabled.')
if not pygame.mixer:
    print('Warning, sound disabled.')

# Directory for game, level, object and animation settings.
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
CONFIG_DIR = os.path.join(MAIN_DIR, '..', 'configs')
IMAGE_DIR = os.path.join(MAIN_DIR, '..', 'images')


# Frame rate at which application is running.
FRAME_RATE = 24

# All characters allowed to be in player's name in highscores table.
PLAYER_NAME_CHARS = (K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9,
                     K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j,
                     K_k, K_l, K_m, K_n, K_o, K_p, K_q, K_r, K_s, K_t,
                     K_u, K_v, K_w, K_x, K_y, K_z)

# Max allowed length for player name in highscores table.
MAX_LEN_PLAYER_NAME = 9

# Debug option to draw collision rects.
DRAW_COLLISION_RECTS = False


class Text:
    """Class to draw text string on the screen."""
    def __init__(self, msg, position, size, colour='white', fontName=None):
        """

        Args:
            msg:      Text string to show on screen.
            position: Tuple with X and Y coordinate defining starting
                      position of the text.
            size:     Font size. Integer.
            colour:   Text color. String ('white', 'red' etc.)
            fontName: Font to use to write the text. String.
        """
        self.msg = msg
        self.position = position
        self.size = size
        self.colour = colour
        self.fontName = fontName
        self.rendered = None
        self.halignment = None
        self.screenWidth = None
        self.font = pygame.font.Font(self.fontName, self.size)

    @property
    def halignment(self):
        """Return horizontal alignment."""
        return self.halignment

    @halignment.setter
    def halignment(self, value):
        """Set horizontal alignment type."""
        if value == 'center':
            textWidth, _ = self.font.size(self.msg)
            posX = int((self.screenWidth - textWidth) / 2)
            self.position = (posX, self.position[1])

    def render(self):
        """Render text."""
        self.rendered = self.font.render(self.msg, True,
                                         pygame.Color(self.colour))

    def draw(self, surface):
        """Draw text on the given surface.

        Args:
            surface: Surface object to draw text on.
        """
        if not self.rendered:
            self.render()

        surface.blit(self.rendered, self.position)


class Game:
    """Main game class."""

    def __init__(self, configDir, imageDir):
        """Initialize game.

        Args:
            configDir: Game settings directory. String.
            imageDir:  Image directory. String.
        """
        self.configDir = configDir
        self.imageDir = imageDir

        self.gameConfig = configparser.ConfigParser()
        self.gameConfig.read(os.path.join(configDir, 'game.conf'))

        self.screenWidth = self.gameConfig['general'].getint('screenWidth')
        self.screenHeight = self.gameConfig['general'].getint('screenHeight')

        pygame.init()
        pygame.display.set_caption('Forggie2')
        self.screen = pygame.display.set_mode((self.screenWidth,
                                               self.screenHeight))

        self.clock = pygame.time.Clock()

        # Menu images.
        self.itemStartOn = None
        self.itemStartOff = None
        self.itemHighscoresOn = None
        self.itemHighscoresOff = None
        self.itemQuitOn = None
        self.itemQuitOff = None
        self.background = None

        # In game on screen text messages.
        self.textLevelTime = None
        self.textLevelCompleted = None
        self.textToNextLevel = None
        self.textLevelFailed = None
        self.textLevelFailed2 = None
        self.textFrogDied = None
        self.textFrogDied2 = None
        self.textCongrats = None
        self.textEnterName = None
        self.textToMenu = None

        # Show borders of menu item images.
        self.debugMenuItems = False

        # Draw rect border in red. Used for debug.
        color = (255, 0, 0)
        self.drawRect = functools.partial(pygame.draw.rect, self.screen, color)

    def renderTexts(self, screenWidth):
        """Render on screen text messages.

        Args:
            screenWidth: Screen width in pixels. integer.
        """
        msg = 'Level time: '
        self.textLevelTime = Text(msg, position=(420, 770), size=30)

        msg = 'Level completed!'
        self.textLevelCompleted = Text(msg, position=(0, 300), size=70)
        self.textLevelCompleted.screenWidth = screenWidth
        self.textLevelCompleted.halignment = 'center'

        msg = 'To proceed to the next level, press <enter>.'
        self.textToNextLevel = Text(msg, position=(0, 350), size=30)
        self.textToNextLevel.screenWidth = screenWidth
        self.textToNextLevel.halignment = 'center'

        msg = 'Level Failed!'
        self.textLevelFailed = Text(msg, position=(0, 190), size=70)
        self.textLevelFailed.screenWidth = screenWidth
        self.textLevelFailed.halignment = 'center'

        msg = "To restart level, press 'r'"
        self.textLevelFailed2 = Text(msg, position=(0, 240), size=30)
        self.textLevelFailed2.screenWidth = screenWidth
        self.textLevelFailed2.halignment = 'center'

        msg = 'Ooops, frog died!'
        self.textFrogDied = Text(msg, position=(0, 190), size=70)
        self.textFrogDied.screenWidth = screenWidth
        self.textFrogDied.halignment = 'center'

        msg = "To continue, press 'c'"
        self.textFrogDied2 = Text(msg, position=(0, 240), size=30)
        self.textFrogDied2.screenWidth = screenWidth
        self.textFrogDied2.halignment = 'center'

        msg = 'Congratulations!'
        self.textCongrats = Text(msg, position=(0, 190), size=70)
        self.textCongrats.screenWidth = screenWidth
        self.textCongrats.halignment = 'center'

        msg = 'Enter your name: '
        self.textEnterName = Text(msg, position=(0, 340), size=30)
        self.textEnterName.screenWidth = screenWidth
        self.textEnterName.halignment = 'center'

        msg = 'Press <enter> to continue to game menu.'
        self.textToMenu = Text(msg, position=(0, 600), size=30)
        self.textToMenu.screenWidth = screenWidth
        self.textToMenu.halignment = 'center'

    def renderAchievedPositionText(self, levelTimes, scores):
        """Render text that shows position achieved.

        Args:
            levelTimes:  List of integers which are times required to
                         finish each level.
            scores:      List of dictionaries with entries from highscore
                         list.

        Returns:
            Object of type Text with rendered text line.
        """
        totalSeconds = sum(levelTimes) / 1000
        minutes = int(totalSeconds / 60)
        seconds = totalSeconds % 60

        onlySeconds = [x['totalSeconds'] for x in scores]
        scorePosition = bisect.bisect(onlySeconds, totalSeconds)
        scorePosition += 1  # Lowest bisect result will be 0.

        if scorePosition == 2:
            scorePositionText = '2nd'
        elif scorePosition == 3:
            scorePositionText = '3rd'
        else:
            scorePositionText = f'{scorePosition}th'

        achievedTime = ''
        if minutes:
            achievedTime = f'{minutes} min '

        seconds = str(seconds)[:5]
        achievedTime += f'{seconds} s'

        if scorePosition == 1:
            msg = f'You set new record time: {achievedTime}'
        elif scorePosition <= 12:
            msg = (f'You have achieved {scorePositionText} '
                   f'best time: {achievedTime}')
        else:
            msg = f'Your completion time is: {achievedTime}'

        textLine = Text(msg, position=(0, 270), size=30)
        textLine.screenWidth = self.screenWidth
        textLine.halignment = 'center'

        return (textLine, scorePosition)

    def play(self, screen, scores):
        """Load level and play it.

        Args:
            screen: Surface object to draw level on.
            scores: All highscores as a list of dictionaries. All
                    scores are sorted from best to worst.
        """
        self.renderTexts(self.screenWidth)
        lifesCfg = self.gameConfig['LifeIndicator']

        # Get from config file the levels defined.
        levels = []
        for level in self.gameConfig['general']['levels'].split(','):
            levels.append(level.strip())

        # Logging configuration.
        logger = Logger(screenWidth=self.screenWidth,
                        screenHeight=self.screenHeight, fontSize=20)

        # By default do not show log messages.
        showLogs = False

        # Elements to enter highscore achiever's name.
        overlay = StaticImage('transparent.png', useAlpha=True)

        clock = pygame.time.Clock()

        # Text object to show what position player achieved.
        textPosition = None

        # Integer saying in which in our highscore would the result fit (1-13).
        scorePosition = None

        # Becomes True if user closes application window.
        quitApplication = False

        # Marks if ESC key was pressed: cancels current game or goes one level
        # up in the main menu.
        pressedEsc = False

        levelsLeft = len(levels)
        gameCompleted = False

        # Store times for each completed level.
        levelTimes = []

        for levelConfigPath in levels:
            levelConfigPath = os.path.join(self.configDir, levelConfigPath)
            print(f"Loading level '{levelConfigPath}'...")

            level = Level(self.configDir, self.imageDir, self.screenWidth,
                          self.screenHeight)
            level.load(levelConfigPath)

            waterObjects = pygame.sprite.RenderPlain(level.floaters)
            trafficCars = pygame.sprite.RenderPlain(level.cars)
            carShadows = pygame.sprite.RenderPlain(level.shadows)

            trafficCarsCollideRects = []
            for car in level.cars:
                trafficCarsCollideRects.append(car.collisionRect)

            floaterCollideRects = []
            for floater in level.floaters:
                floaterCollideRects.append(floater.collisionRect)

            lifeIndicator = LifeIndicator(lifesCfg, self.configDir,
                                          self.imageDir)

            groundObjects = pygame.sprite.OrderedUpdates(level.background,
                                                         level.finishImage,
                                                         waterObjects)

            highscoreOverlay = pygame.sprite.OrderedUpdates(overlay)

            frog = level.frog

            msg = '%s: Level %s' % (self.gameConfig['general']['name'],
                                    level.name)
            pygame.display.set_caption(msg)

            msg = 'Level: ' + level.name
            textLevelName = Text(msg, position=(5, 770), size=30)

            # Holds player name after the completion of the game.
            playerName = ''

            # Marks if frog ran out of lifes.
            gameOver = False

            # Marks if level is completed.
            levelCompleted = False

            # Temporary value to calculate the period of inactivity.
            inactiveTimeStart = None

            currentTime = pygame.time.get_ticks()
            inactiveTime = currentTime
            levelTime = currentTime - inactiveTime

            screen = self.screen

            going = True
            while going and not (quitApplication or pressedEsc):
                clock.tick(FRAME_RATE)

                for event in pygame.event.get():
                    if event.type == QUIT:
                        print('Quiting application!')
                        quitApplication = True

                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pressedEsc = True

                        if event.key in (K_RETURN, K_KP_ENTER):
                            if levelCompleted:
                                inactiveTimeStart = 0
                                going = False

                        elif event.key == K_UP:
                            frog.pressedUp = True

                        elif event.key == K_DOWN:
                            frog.pressedDown = True

                        elif event.key == K_LEFT:
                            frog.pressedLeft = True

                        elif event.key == K_RIGHT:
                            frog.pressedRight = True

                        elif (event.key == K_c
                              and (frog.isDead or frog.isDrowned)
                              and not gameOver):
                            frog.pressedUp = False
                            frog.pressedDown = False
                            frog.pressedLeft = False
                            frog.pressedRight = False

                            frog.isDead = False
                            frog.isDrowned = False
                            frog.moveToStart()

                            inactiveTime += (pygame.time.get_ticks()
                                             - inactiveTimeStart)
                            inactiveTimeStart = 0

                        elif event.key == K_r and gameOver:
                            frog.pressedUp = False
                            frog.pressedDown = False
                            frog.pressedLeft = False
                            frog.pressedRight = False

                            gameOver = False
                            frog.isDead = False
                            frog.isDrowned = False
                            frog.lifesLeft = 3
                            frog.moveToStart()
                            lifeIndicator.resetLifes()

                            inactiveTime += (pygame.time.get_ticks()
                                             - inactiveTimeStart)
                            inactiveTimeStart = 0

                        elif event.key == K_BACKQUOTE:
                            # Turn on/off showing log messages on top of the
                            # screen.
                            showLogs = not showLogs

                        elif gameCompleted and event.key in PLAYER_NAME_CHARS:
                            if len(playerName) < MAX_LEN_PLAYER_NAME:
                                playerName += chr(event.key)

                        elif gameCompleted and event.key == K_BACKSPACE:
                            playerName = playerName[:-1]

                frogCollide = frog.collisionRect.collidelist

                collisionWithCars = frogCollide(trafficCarsCollideRects)

                finishRect = level.finishImage.collisionRect
                collisionsWithFinish = frog.collisionRect.colliderect(
                    finishRect)

                if level.riverTrackRects:
                    collisionWithRiver = frogCollide(level.riverTrackRects)
                    logger.log(f'collisionWithRiver: {collisionWithRiver}')
                else:
                    collisionWithRiver = None

                collisionWithFloaters = frogCollide(floaterCollideRects)

                # Clear area under sprites.
                waterObjects.clear(screen, level.background)

                waterObjects.update()
                trafficCars.update()

                groundObjects.draw(screen)

                if DRAW_COLLISION_RECTS:
                    for floater in level.floaters:
                        pygame.draw.rect(screen, (255, 0, 0), floater.rect, 1)

                    for carRect in trafficCarsCollideRects:
                        pygame.draw.rect(screen, (255, 0, 0), carRect, 1)

                frog.update(collisionWithCars, collisionWithRiver,
                            collisionWithFloaters, level.floaters,
                            level.riverTracks)
                frog.draw(screen)

                carShadows.draw(screen)
                trafficCars.draw(screen)

                if not (frog.isDead or frog.isDrowned) and not levelCompleted:
                    currentTime = pygame.time.get_ticks()
                    levelTime = currentTime - inactiveTime

                # Show lifes' indicator.
                lifeIndicator.update(frog)
                lifeIndicator.draw(screen)

                textLevelName.draw(screen)
                self.textLevelTime.draw(screen)

                # Show level time.
                font = pygame.font.Font(None, 30)
                timeRendered = font.render(str(round(levelTime / 1000.0, 1)),
                                           True, pygame.Color('white'))
                screen.blit(timeRendered, (535, 770))

                # Show level completion message.
                if collisionsWithFinish:
                    if not levelCompleted:
                        levelTimes.append(levelTime)
                        levelsLeft -= 1
                        if levelsLeft == 0:
                            gameCompleted = True

                    levelCompleted = True
                    frog.isLocked = True

                    if not gameCompleted:
                        self.textLevelCompleted.draw(screen)
                        self.textToNextLevel.draw(screen)

                elif (frog.isDead or frog.isDrowned) and frog.lifesLeft == 0:
                    msg = 'Game Over. All lifes lost!'
                    logger.log(msg, screen)
                    gameOver = True
                    self.textLevelFailed.draw(screen)
                    self.textLevelFailed2.draw(screen)

                    if not inactiveTimeStart:
                        inactiveTimeStart = pygame.time.get_ticks()

                elif (frog.isDead or frog.isDrowned) and not gameOver:
                    self.textFrogDied.draw(screen)
                    self.textFrogDied2.draw(screen)

                    if not inactiveTimeStart:
                        inactiveTimeStart = pygame.time.get_ticks()

                if gameCompleted:
                    highscoreOverlay.draw(screen)
                    self.textCongrats.draw(screen)

                    if not textPosition:
                        textPosition, scorePosition = \
                                self.renderAchievedPositionText(levelTimes,
                                                                scores)

                    textPosition.draw(screen)

                    # Request to enter player's name, if result is good enough
                    # to go to the highscore board.
                    if scorePosition <= 12:
                        self.textEnterName.draw(screen)

                        textPlayerName = Text(playerName, position=(0, 370),
                                              size=45)
                        textPlayerName.screenWidth = self.screenWidth
                        textPlayerName.halignment = 'center'
                        textPlayerName.draw(screen)

                    self.textToMenu.draw(screen)

                if showLogs:
                    logger.displayMessages(screen)

                pygame.display.flip()

            if quitApplication:
                break

        print(f'LevelTimes: {levelTimes}')

        if gameCompleted:
            totalSeconds = sum(levelTimes) / 1000
            minutes = int(totalSeconds / 60)
            seconds = totalSeconds % 60

            score = {'totalSeconds': totalSeconds,
                     'name': playerName,
                     'minutes': minutes,
                     'seconds': seconds,
                     }
        else:
            score = None

        print(f'score: {score}')
        return score, quitApplication, pressedEsc

    def loadMenuImages(self):
        """Load menu images."""
        self.itemStartOn = StaticImage('menu_start_on.png')
        self.itemStartOn.rect.topleft = (100, 200)

        self.itemStartOff = StaticImage('menu_start_off.png')
        self.itemStartOff.rect.topleft = (100, 200)

        self.itemHighscoresOn = StaticImage('menu_highscores_on.png')
        self.itemHighscoresOn.rect.topleft = (100, 300)

        self.itemHighscoresOff = StaticImage('menu_highscores_off.png')
        self.itemHighscoresOff.rect.topleft = (100, 300)

        self.itemQuitOn = StaticImage('menu_quit_on.png')
        self.itemQuitOn.rect.topleft = (100, 400)

        self.itemQuitOff = StaticImage('menu_quit_off.png')
        self.itemQuitOff.rect.topleft = (100, 400)

        self.background = StaticImage('menu_background.png')

    def showMenu(self):
        """Show menu and highscores table."""
        self.loadMenuImages()

        # Menu items when first item is active.
        menuItems1 = pygame.sprite.OrderedUpdates(self.itemStartOn,
                                                  self.itemHighscoresOff,
                                                  self.itemQuitOff)

        # Menu items when second item is active.
        menuItems2 = pygame.sprite.OrderedUpdates(self.itemStartOff,
                                                  self.itemHighscoresOn,
                                                  self.itemQuitOff)

        # Menu items when third item is active.
        menuItems3 = pygame.sprite.OrderedUpdates(self.itemStartOff,
                                                  self.itemHighscoresOff,
                                                  self.itemQuitOn)

        backgroundObjects = pygame.sprite.OrderedUpdates(self.background)

        scorePath = self.gameConfig['general'].get('highscorePath')

        highscores = Highscores()
        highscores.load(scorePath)
        highscores.render()

        menuLevel = 1
        menuItemActive = 1

        showHighScores = False
        quitApplication = False
        going = True
        while going and not quitApplication:
            self.clock.tick(FRAME_RATE)

            for event in pygame.event.get():
                if event.type == QUIT:
                    quitApplication = True

                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        menuLevel -= 1
                        showHighScores = False

                    if event.key in (K_RETURN, K_KP_ENTER):
                        if menuItemActive == 3:
                            quitApplication = True

                        elif menuItemActive == 2:
                            menuLevel += 1
                            showHighScores = True

                        elif menuItemActive == 1:
                            score, quitApplication, pressedEsc = self.play(
                                self.screen, highscores.scores)

                            if quitApplication:
                                print('Quitting application...')
                                pygame.quit()
                                sys.exit(0)

                            # Save score only if user left level by pressing
                            # <enter> key.
                            if score and not pressedEsc:
                                highscores.scores.append(score)
                                highscores.render()
                                highscores.save(scorePath)

                    elif event.key == K_UP:
                        menuItemActive -= 1

                        if menuItemActive < 1:
                            menuItemActive = 3

                    elif event.key == K_DOWN:
                        menuItemActive += 1

                        if menuItemActive > 3:
                            menuItemActive = 1

            backgroundObjects.draw(self.screen)

            if showHighScores:
                highscores.draw(self.screen)
                pygame.display.flip()
                continue

            if menuLevel == 0:
                quitApplication = True

            if menuItemActive == 1:
                menuItems1.draw(self.screen)

            elif menuItemActive == 2:
                menuItems2.draw(self.screen)

            elif menuItemActive == 3:
                menuItems3.draw(self.screen)

            # For debuging purposes
            if self.debugMenuItems:
                self.drawRect(self.itemStartOn.rect, 1)
                self.drawRect(self.itemStartOff.rect, 1)
                self.drawRect(self.itemHighscoresOn.rect, 1)
                self.drawRect(self.itemHighscoresOff.rect, 1)
                self.drawRect(self.itemQuitOn.rect, 1)
                self.drawRect(self.itemQuitOff.rect, 1)

            pygame.display.flip()

        if quitApplication:
            print('Quitting application...')
            pygame.quit()
            sys.exit(0)


def main():
    """Entry point to start the game."""
    game = Game(CONFIG_DIR, IMAGE_DIR)
    game.showMenu()


if __name__ == '__main__':
    main()
