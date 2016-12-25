import cv2
import os
import math

from hero_detector import HeroDetector
from red_team import RedTeam
from blue_team import BlueTeam

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

  def detect(self):
    self.hero_detector.draw_divider()

    for hero in self.__class__.heroes:
      path = os.path.abspath('src/heroes/' + hero + '.png')
      template = cv2.imread(path)
      template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
      h, w = template.shape[:2]
      points = self.hero_detector.detect(template)

      for point1 in points:
        if self.have_seen_position(point1):
          continue

        if self.hero_detector.is_red_team(point1[1]):
          self.red_team.add(hero, point1[0])
        else:
          self.blue_team.add(hero, point1[0])

        point2 = (point1[0] + w, point1[1] + h)
        cv2.rectangle(self.original, point1, point2, self.color, self.thickness)

  def have_seen_position(self, point):
    round_point = (self.round(point[0]), self.round(point[1]))

    if round_point in self.seen_positions:
      return True

    self.seen_positions.append(round_point)
    return False

  def round(self, num):
    return int(math.ceil(num / 40.0)) * 40
