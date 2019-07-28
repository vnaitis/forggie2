"""Tests for class Car."""
import copy
import mock
import pytest
import pygame
import random

from context import car

class FakeCar(car.Car):
    """Fake Frog class to test methods."""
    def __init__(self):
        pass

class FakeImage(object):
    def __init__(self):
        self.rect = None
        self.collisionRect = None
        self.moveDistance = None


@pytest.mark.parametrize(('speed,direction,rect,collisionRect,shadowRect,'
                          'expRect,expCollRect,expShadowRect'),
    (
        (10, 'to_left',
         pygame.Rect(200, 300, 30, 40), # rect
         pygame.Rect(200, 300, 30, 40), # collisionRect
         pygame.Rect(200, 300, 30, 40), # shadowRect

         pygame.Rect(210, 300, 30, 40), # expRect
         pygame.Rect(215, 307, 30, 40), # expCollRect
         pygame.Rect(210, 296, 30, 40), # expShadowRect
        ),
        (-10, 'to_left',
         pygame.Rect(200, 300, 30, 40), # rect
         pygame.Rect(200, 300, 30, 40), # collisionRect
         pygame.Rect(200, 300, 30, 40), # shadowRect

         pygame.Rect(190, 300, 30, 40), # expRect
         pygame.Rect(195, 307, 30, 40), # expCollRect
         pygame.Rect(190, 296, 30, 40), # expShadowRect
        ),
        # Check if car is moved back to the other side of the screen.
        (-10, 'to_left',
         pygame.Rect(-81, 300, 30, 40), # rect
         pygame.Rect(-11, 310, 30, 40), # collisionRect
         pygame.Rect(-21, 290, 30, 40), # shadowRect

         pygame.Rect(609, 293, 30, 40), # expRect
         pygame.Rect(614, 300, 30, 40), # expCollRect
         pygame.Rect(609, 289, 30, 40), # expShadowRect
        ),

        (10, 'to_right',
         pygame.Rect(200, 300, 30, 40), # rect
         pygame.Rect(200, 300, 30, 40), # collisionRect
         pygame.Rect(200, 300, 30, 40), # shadowRect

         pygame.Rect(210, 300, 30, 40), # expRect
         pygame.Rect(215, 307, 30, 40), # expCollRect
         pygame.Rect(210, 296, 30, 40), # expShadowRect
        ),
        (-10, 'to_right',
         pygame.Rect(190, 300, 30, 40), # rect
         pygame.Rect(190, 300, 30, 40), # collisionRect
         pygame.Rect(190, 300, 30, 40), # shadowRect

         pygame.Rect(180, 300, 30, 40), # expRect
         pygame.Rect(185, 307, 30, 40), # expCollRect
         pygame.Rect(180, 296, 30, 40), # expShadowRect
        ),
        # Check if car is moved back to the other side of the screen.
        (10, 'to_right',
         pygame.Rect(650, 300, 30, 40), # rect
         pygame.Rect(591, 300, 30, 40), # collisionRect
         pygame.Rect(591, 300, 30, 40), # shadowRect

         pygame.Rect(-40, 293, 30, 40), # expRect
         pygame.Rect(-35, 300, 30, 40), # expCollRect
         pygame.Rect(-40, 289, 30, 40), # expShadowRect
        ),
    ),
    ids=('TEST1_CASE1', 'TEST1_CASE2', 'TEST1_CASE3', 'TEST1_CASE4',
         'TEST1_CASE5', 'TEST1_CASE6')
)
def test_car_update(speed, direction, rect, collisionRect, shadowRect, expRect,
                    expCollRect, expShadowRect):
    """Tests for Car.update()"""
    car = FakeCar()
    car.screenWidth = 600
    car.direction = direction
    car.speed = speed
    car.carWidth = rect.width
    car.rect = rect
    car.collisionRect = collisionRect
    car.shadow = FakeImage() 
    car.shadow.rect = copy.deepcopy(rect)
    car.roadTop = 290
    car.roadTopGap = 3
    car.freeVerticalSpace = 5
    car.crMarginLeft = 5
    car.crMarginTop = 7

    random.randint = mock.MagicMock(return_value=3)

    car.update()

    msg = "Expected rect '%s', but got '%s'" % (expRect, car.rect)
    assert car.rect == expRect, msg

    msg = "Expected collision rect '%s', but got '%s'"
    msg = msg % (expCollRect, car.collisionRect)
    assert car.collisionRect == expCollRect, msg

    msg = "Expected shadow rect '%s', but got '%s'"
    msg = msg % (expShadowRect, car.shadow.rect)
    assert car.shadow.rect == expShadowRect, msg

