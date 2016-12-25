import cv2
import os

from src.models.hero_detector import HeroDetector
from src.models.red_team import RedTeam
from src.models.blue_team import BlueTeam

class TeamDetector:
  # TODO: mei
  heroes = ['ana', 'bastion', 'dva', 'genji', 'hanzo', 'junkrat', 'lucio',
            'mccree', 'mercy', 'pharah', 'reaper', 'reinhardt', 'roadhog',
            'soldier-76', 'sombra', 'symmetra', 'torbjorn', 'tracer',
            'widowmaker', 'winston', 'zarya', 'zenyatta', 'unknown']

  def __init__(self, original):
    self.red_team = RedTeam([])
    self.blue_team = BlueTeam([])
    self.original = original
    self.thickness = 2
    self.color = (255, 0, 0)
    self.hero_detector = HeroDetector(self.original)
    self.seen_positions = []

  # Look in the original image for each Overwatch hero.
  def detect(self, draw_boxes=False):
    for hero in self.__class__.heroes:
      self.detect_hero(hero, draw_boxes=draw_boxes)

  # Look for the given hero in the original image.
  def detect_hero(self, hero, draw_boxes=False):
    path = os.path.abspath('src/heroes/' + hero + '.png')
    template = cv2.imread(path)
    (height, width) = template.shape[:2]
    points = self.hero_detector.detect(template)

    if points is None:
      return

    for top_left_point in points:
      if self.have_seen_position(top_left_point):
        return

      if self.hero_detector.is_red_team(top_left_point[1]):
        self.red_team.add(hero, top_left_point[0])
      else:
        self.blue_team.add(hero, top_left_point[0])

      if draw_boxes:
        bottom_right_point = (top_left_point[0] + width, top_left_point[1] + height)
        cv2.rectangle(self.original, top_left_point, bottom_right_point, \
                      self.color, self.thickness)

  def have_seen_position(self, point):
    if point in self.seen_positions:
      return True

    self.seen_positions.append(point)
    return False
