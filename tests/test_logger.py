"""Tests for Logger class."""
import pytest
import pygame

from context import logger

# Need to initialize pygame parts (like pygame.font.init()) or the whole
# pygame with pygame.init().
pygame.init()


@pytest.mark.parametrize('msg,count,expected',
    (
        (None, 2, []),
        ('', 2, ['']),
        ('123456', 0, ['123456']),
        ('123', 3, ['1', '2', '3']),
        ('1234', 3, ['1', '2', '3', '4']),
        ('12345', 3, ['1', '2', '3', '4', '5']),
        ('123456', 3, ['12', '34', '56']),
        ('1234567890123456789012', 3, ['1234567', '8901234', '5678901', '2']),
        ('1234567890123456789012', 2.5, ['12345678', '90123456', '789012']),
    ),
    ids=('TEST1_CASE1', 'TEST1_CASE2', 'TEST1_CASE3', 'TEST1_CASE4',
         'TEST1_CASE5', 'TEST1_CASE6', 'TEST1_CASE7', 'TEST1_CASE8',
         'TEST1_CASE9'),
)
def test_Logger_splitText(msg, count, expected):
    """Tests for Logger.splitText()

    Logger.splitText() uses pygame.font, so pygame.font.init() must be called
    for these tests to work.
    """
    loger = logger.Logger(screenWidth=640, screenHeight=800)
    result = loger.splitText(msg, count)

    msg = "expected '%s', but got '%s'" % (expected, result)
    assert result == expected, msg


@pytest.mark.parametrize('msg,logToScreen,logToStdout,expReturn,expected',
    (
        ('abc', False, False, None, []),
        ('abc', False, True, None, []),

        (('This module contains several simple classes to be used within '
          'games. There is the main Sprite class and several Group classes '
          'that contain Sprites.'),
         True, False, None,
         [('This module contains several simple classes to be used within '
           'games. There is the main Sprite class '),
           'and several Group classes that contain Sprites.']
        ),

    ),
    ids=('TEST2_CASE1', 'TEST2_CASE2', 'TEST2_CASE3'),
)

def test_Logger_log(msg, logToScreen, logToStdout, expReturn, expected):
    """Tests for Logger.log()

    Logger.log() uses pygame.font, so pygame.font.init() must be called
    for these tests to work.
    """
    loger = logger.Logger(screenWidth=640, screenHeight=800)
    result = loger.log(msg, logToScreen=logToScreen, logToStdout=logToStdout)

    msg = "expected '%s', but got '%s'" % (expReturn, result)
    assert expReturn == result, msg

    msg = "expected '%s', but got '%s'" % (expected, loger.messages)
    assert expected == loger.messages, msg

