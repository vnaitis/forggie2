"""Class to deal with highscores."""
import os
import datetime
import traceback
import configparser
import pygame


class Highscores:
    """Class to load show and save highscore data."""

    def __init__(self):
        """Initialize object."""
        # Max amount of entries in highscores table (and highscores.conf).
        self.maxEntries = 12

        font = pygame.font.Font(None, 70)
        self.title = font.render('Highscores', True, pygame.Color('white'))

        font = pygame.font.Font(None, 50)
        self.textMin = font.render('min', True, pygame.Color('white'))
        self.textS = font.render('s', True, pygame.Color('white'))

        self.scores = []
        self.rendered = []

    def load(self, cfgpath):
        """Load highscores.

        Args:
            cfgpath: Path to the file with highscores. String.
        """
        cfg = configparser.ConfigParser()
        cfg.read(cfgpath)

        if not os.path.exists(cfgpath):
            msg = f"WARNING: No '{cfgpath}' found. Will create one if needed."
            print(msg)
            return

        sectionNotPresent = False
        try:
            for i in range(1, self.maxEntries + 1):
                try:
                    section = cfg['result' + str(i)]
                except KeyError:
                    # Probably there is less than 12 entries in highscore
                    # table, so there is no point continuing trying to get
                    # them.
                    break

                # Limit the length of the name to 9 characters.
                name = section.get('name')[:9]

                # Convert time into minutes and seconds.
                totalSeconds = section.getfloat('time')

                minutes = int(totalSeconds / 60)
                seconds = totalSeconds % 60

                new = {'totalSeconds': totalSeconds,
                       'name': name,
                       'minutes': minutes,
                       'seconds': seconds,
                       }
                self.scores.append(new)
        except Exception:
            # Whatever happens, we don't want it to prevent from running the
            # program, because highscores is not a vital part of the program.
            if sectionNotPresent:
                return
            traceback.print_exc()
            if os.path.exists(cfgpath):
                now = datetime.datetime.now()
                backupName = '%s.bck.%s' % (cfgpath, now.timestamp())
                msg = (f"ERROR: Highscore data in file '{cfgpath}' is "
                       f"not in expected format. Renaming '{cfgpath}' "
                       f"to '{backupName}'. New '{cfgpath}' file "
                       "will be created for new results.")
                print(msg)
                os.rename(cfgpath, backupName)
            else:
                msg = (f"WARNING:'{cfgpath}' does not exist. Will create "
                       "one if needed.")
                print(msg)

    def save(self, filepath):
        """Write highscores to a file.

        Args:
            filepath:  Path to the file to save results to. String.
        """
        self.scores.sort(key=lambda x: x['totalSeconds'])

        # We keep only best results that would fit our highscore table.
        self.scores = self.scores[:self.maxEntries]

        with open(filepath, 'w') as scoreFile:
            txt = (f'# This file must have {self.maxEntries} entries.\n'
                   f'# name - max 9 characters.\n'
                   f'# time - time in seconds.\n\n')
            scoreFile.write(txt)

            for idx, score in enumerate(self.scores, 1):
                scoreFile.write(f'[result{idx}]\n')
                scoreFile.write(f"name = {score['name']}\n")
                scoreFile.write(f"time = {score['totalSeconds']}\n\n")

    def render(self):
        """Render highscore text lines."""
        # Sort and keep best entries only.
        self.scores.sort(key=lambda x: x['totalSeconds'])
        self.scores = self.scores[:self.maxEntries]

        font = pygame.font.Font(None, 50)

        self.rendered = []
        for idx, item in enumerate(self.scores, 1):
            text = str(idx) + '.'
            textNumber = font.render(text, True, pygame.Color('white'))

            textName = font.render(item['name'], True, pygame.Color('white'))

            if item['minutes']:
                text = f"{item['minutes']}"
                textMinutes = font.render(text, True, pygame.Color('white'))
            else:
                textMinutes = None

            # Limit length to avoid cases like '21.80000000000001 s'.
            text = str(item['seconds'])[:5]
            textSeconds = font.render(text, True, pygame.Color('white'))

            tmp = (textNumber, textName, textMinutes, textSeconds)
            self.rendered.append(tmp)

    def draw(self, surface):
        """Draw rendered text lines on the surface.

        Args:
            surface: Surface object to draw highscores onto.
        """
        surface.blit(self.title, (80, 25))

        coordY = 50
        for number, name, minutes, seconds in self.rendered:
            coordY += 50
            surface.blit(number, (50, coordY))
            surface.blit(name, (110, coordY))
            if minutes:
                surface.blit(minutes, (330, coordY))
                surface.blit(self.textMin, (375, coordY))
            surface.blit(seconds, (460, coordY))
            surface.blit(self.textS, (550, coordY))
