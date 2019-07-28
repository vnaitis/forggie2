"""Tests for functions in forggie2.py."""
import pytest
import pygame

from context import frog


class FakeFrog(frog.Frog):
    """Fake Frog class to test methods."""
    def __init__(self):
        pass

class FakeImage(object):
    def __init__(self):
        self.rect = None
        self.collisionRect = None
        self.moveDistance = None


@pytest.mark.parametrize('speed,rect,collisionRect,expRect,expCollRect',
    (
        (-2,
         pygame.Rect(72, 181, 40, 44),
         pygame.Rect(102, 181, 40, 44),
         pygame.Rect(70, 181, 40, 44),
         pygame.Rect(100, 181, 40, 44),
        ),
        (-2,
         pygame.Rect(0, 181, 40, 44),
         pygame.Rect(0, 181, 40, 44),
         pygame.Rect(0, 181, 40, 44),
         pygame.Rect(0, 181, 40, 44),
        ),
        (2,
         pygame.Rect(72, 181, 40, 44),
         pygame.Rect(102, 181, 40, 44),
         pygame.Rect(74, 181, 40, 44),
         pygame.Rect(104, 181, 40, 44),
        ),
        (2,
         pygame.Rect(560, 181, 40, 44),
         pygame.Rect(560, 181, 40, 44),
         pygame.Rect(560, 181, 40, 44),
         pygame.Rect(560, 181, 40, 44),
        ),
    ),
    ids=('TEST1_CASE1', 'TEST1_CASE2', 'TEST1_CASE3', 'TEST1_CASE4')
)
def test_frog_move(speed, rect, collisionRect, expRect, expCollRect):
    """Tests for Frog.move()"""
    frog = FakeFrog()
    frog.screenWidth = 600
    frog.anim = FakeImage()
    frog.anim.rect = rect
    frog.anim.collisionRect = collisionRect

    frog.move(speed)

    msg = "Expected rect '%s', but got '%s'" % (expRect, frog.anim.rect)
    assert frog.anim.rect == expRect, msg

    msg = "Expected collision rect '%s', but got '%s'"
    msg = msg % (expCollRect, frog.anim.collisionRect)
    assert frog.anim.collisionRect == expCollRect, msg


@pytest.mark.parametrize('distance,rect,collisionRect,expRect,expCollRect',
    (
        # Not reaching top.
        (10,
         pygame.Rect(300, 602, 122, 70),
         pygame.Rect(305, 617, 30, 40),
         pygame.Rect(300, 592, 122, 70),
         pygame.Rect(305, 607, 30, 40),
        ),
        # Going over top.
        (10,
         pygame.Rect(300, 2, 122, 70),
         pygame.Rect(305, 8, 30, 40),
         pygame.Rect(300, -6, 122, 70),
         pygame.Rect(305, 0, 30, 40),
        ),
        # Reaching top exactly.
        (10,
         pygame.Rect(300, 15, 122, 70),
         pygame.Rect(305, 0, 30, 40),
         pygame.Rect(300, 15, 122, 70),
         pygame.Rect(305, 0, 30, 40),
        ),
    ),
    ids=('TEST2_CASE1', 'TEST2_CASE2', 'TEST2_CASE3')
)
def test_frog_moveUp(distance, rect, collisionRect, expRect, expCollRect):
    """Tests for Frog.moveUp()"""
    frog = FakeFrog()
    frog.screenWidth = 600
    frog.anim = FakeImage()
    frog.anim.rect = rect
    frog.anim.collisionRect = collisionRect
    frog.anim.moveDistance = distance

    frog.moveUp()

    msg = "Expected rect '%s', but got '%s'" % (expRect, frog.anim.rect)
    assert frog.anim.rect == expRect, msg

    msg = "Expected collision rect '%s', but got '%s'"
    msg = msg % (expCollRect, frog.anim.collisionRect)
    assert frog.anim.collisionRect == expCollRect, msg


@pytest.mark.parametrize('distance,rect,collisionRect,expRect,expCollRect',
    (
        # Not reaching bottom.
        (10,
         pygame.Rect(300, 602, 122, 70),
         pygame.Rect(305, 617, 30, 40),
         pygame.Rect(300, 612, 122, 70),
         pygame.Rect(305, 627, 30, 40),
        ),
        # Going below bottom.
        (10,
         pygame.Rect(300, 740, 122, 70),
         pygame.Rect(305, 755, 30, 40),
         pygame.Rect(300, 745, 122, 70),
         pygame.Rect(305, 760, 30, 40),
        ),
        # Reaching bottom exactly.
        (10,
         pygame.Rect(300, 745, 122, 70),
         pygame.Rect(305, 760, 30, 40),
         pygame.Rect(300, 745, 122, 70),
         pygame.Rect(305, 760, 30, 40),
        ),
    ),
    ids=('TEST3_CASE1', 'TEST3_CASE2', 'TEST3_CASE3')
)
def test_frog_moveDown(distance, rect, collisionRect, expRect, expCollRect):
    """Tests for Frog.moveDown()"""
    frog = FakeFrog()
    frog.screenHeight = 800
    frog.anim = FakeImage()
    frog.anim.rect = rect
    frog.anim.collisionRect = collisionRect
    frog.anim.moveDistance = distance

    frog.moveDown()

    msg = "Expected rect '%s', but got '%s'" % (expRect, frog.anim.rect)
    assert frog.anim.rect == expRect, msg

    msg = "Expected collision rect '%s', but got '%s'"
    msg = msg % (expCollRect, frog.anim.collisionRect)
    assert frog.anim.collisionRect == expCollRect, msg


@pytest.mark.parametrize('distance,rect,collisionRect,expRect,expCollRect',
    (
        # Not reaching left edge.
        (10,
         pygame.Rect(300, 602, 122, 70),
         pygame.Rect(305, 617, 30, 40),
         pygame.Rect(290, 602, 122, 70),
         pygame.Rect(295, 617, 30, 40),
        ),
        # Going over left edge.
        (10,
         pygame.Rect(20, 740, 122, 70),
         pygame.Rect(5, 755, 30, 40),
         pygame.Rect(15, 740, 122, 70),
         pygame.Rect(0, 755, 30, 40),
        ),
        # Reaching left edge exactly.
        (10,
         pygame.Rect(15, 745, 122, 70),
         pygame.Rect(0, 760, 30, 40),
         pygame.Rect(15, 745, 122, 70),
         pygame.Rect(0, 760, 30, 40),
        ),
    ),
    ids=('TEST4_CASE1', 'TEST4_CASE2', 'TEST4_CASE3')
)
def test_frog_moveLeft(distance, rect, collisionRect, expRect, expCollRect):
    """Tests for Frog.moveLeft()"""
    frog = FakeFrog()
    frog.anim = FakeImage()
    frog.anim.rect = rect
    frog.anim.collisionRect = collisionRect
    frog.anim.moveDistance = distance

    frog.moveLeft()

    msg = "Expected rect '%s', but got '%s'" % (expRect, frog.anim.rect)
    assert frog.anim.rect == expRect, msg

    msg = "Expected collision rect '%s', but got '%s'"
    msg = msg % (expCollRect, frog.anim.collisionRect)
    assert frog.anim.collisionRect == expCollRect, msg


@pytest.mark.parametrize('distance,rect,collisionRect,expRect,expCollRect',
    (
        # Not reaching right edge.
        (10,
         pygame.Rect(300, 602, 122, 70),
         pygame.Rect(305, 617, 30, 40),
         pygame.Rect(310, 602, 122, 70),
         pygame.Rect(315, 617, 30, 40),
        ),
        # Going over right edge.
        (10,
         pygame.Rect(550, 740, 122, 70),
         pygame.Rect(565, 755, 30, 40),
         pygame.Rect(555, 740, 122, 70),
         pygame.Rect(570, 755, 30, 40),
        ),
        # Reaching right edge exactly.
        (10,
         pygame.Rect(555, 745, 122, 70),
         pygame.Rect(570, 760, 30, 40),
         pygame.Rect(555, 745, 122, 70),
         pygame.Rect(570, 760, 30, 40),
        ),
    ),
    ids=('TEST5_CASE1', 'TEST5_CASE2', 'TEST5_CASE3')
)
def test_frog_moveRight(distance, rect, collisionRect, expRect, expCollRect):
    """Tests for Frog.moveLeft()"""
    frog = FakeFrog()
    frog.screenWidth = 600
    frog.anim = FakeImage()
    frog.anim.rect = rect
    frog.anim.collisionRect = collisionRect
    frog.anim.moveDistance = distance

    frog.moveRight()

    msg = "Expected rect '%s', but got '%s'" % (expRect, frog.anim.rect)
    assert frog.anim.rect == expRect, msg

    msg = "Expected collision rect '%s', but got '%s'"
    msg = msg % (expCollRect, frog.anim.collisionRect)
    assert frog.anim.collisionRect == expCollRect, msg

