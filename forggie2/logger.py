"""Class to print log messages on top of the game screen."""
import pygame


class Logger:
    """Class to log on top of the game screen."""

    def __init__(self, screenWidth, screenHeight, fontSize=20, topMargin=2,
                 bottomMargin=2, leftMargin=2, rightMargin=2):
        """Initialize logger.

        Args:
            screenWidth:  Game screen width in pixels. Integer.
            screenHeight: Game screen height in pixels. Integer.
            fontSize:     Text size in pixels. Integer.
            topMargin:    Top margin in pixels. Integer.
            bottomMargin: Bottom margin in pixels. Integer.
            leftMargin:   Left margin in pixels. Integer.
            rightMargin:  Right margin in pixels. Integer.
        """
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self.fontSize = fontSize
        self.antialias = True
        self.textColour = (255, 255, 255)

        # Selects default font.
        self.font = pygame.font.Font(None, self.fontSize)

        # Margins to leave from screen edges when displaying messages.
        self.topMargin = topMargin
        self.bottomMargin = bottomMargin
        self.leftMargin = leftMargin
        self.rightMargin = rightMargin

        # All (split) messages to be shown on screen.
        self.messages = []

        # Max amount of messages to store in self.messages.
        self.messageBufferSize = 100

        # Count of newest entries from the log message buffer to show on
        # screen.
        self.messageShowCount = 35

        # X, Y coordinates of the message.
        self.msgX = 10
        self.msgY = 10

        # Vertical gap in pixels between Y coordinates of two adjacent text
        # lines.
        self.verticalGap = 20

    @staticmethod
    def splitText(msg, count):
        """Split line of text into chunks to fit screen.

        Args:
            msg:   Message as a string of text.
            count: Amount of parts to divided message to.

        Returns:
            Initial string split into a list of text strings.
        """
        if count <= 1:
            return [msg]

        if msg is None:
            return []

        result = []

        # Amount of characters that fit into one line (i.e. max line length).
        length = int(len(msg) / count)

        while len(msg) > length:
            result.append(msg[:length])
            msg = msg[length:]

        # Append last part of the message.
        result.append(msg)

        return result

    def log(self, msg, logToScreen=True, logToStdout=False):
        """Save message to the log message buffer.

        Args:
            msg:         Text string to be logged.
            logToScreen: Boolean value to tell if log message should apear
                         on top of the game screen.
            logToStdout: Boolean value to tell if the log message should be
                         logged to stdout.

        Returns:
            None.
        """
        if logToStdout is True:
            print(msg)
            return

        if not logToScreen:
            return

        # Decrease message buffer size to the configured size.
        if len(self.messages) > self.messageBufferSize:
            self.messages = self.messages[:self.messageBufferSize]

        # Screen width in pixels available to put a string of text.
        availableWidth = self.screenWidth - self.leftMargin - self.rightMargin

        # Width (and height) of our string in pixels.
        width, _ = self.font.size(msg)

        # Amount of times we need to split our message in order to fit it.
        splitCount = float(width / availableWidth)

        # Our message divided into parts.
        divided = self.splitText(msg, splitCount)

        self.messages = self.messages + divided

    def displayMessages(self, screen):
        """Display stored messages on the screen.

        Args:
            screen: Pygame screen object.

        Returns:
            None.
        """
        xPos = self.msgX
        yPos = self.msgY

        for msg in self.messages[-self.messageShowCount:]:
            rendered = self.font.render(msg, self.antialias, self.textColour)
            screen.blit(rendered, (xPos, yPos))
            yPos += self.verticalGap
