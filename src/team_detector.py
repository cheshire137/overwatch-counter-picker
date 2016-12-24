import cv2
import os
from hero_detector import HeroDetector

class TeamDetector:
  # TODO: symmetra, hanzo, sombra, pharah, mei, winston
  heroes = ['ana', 'bastion', 'dva', 'genji', 'junkrat', 'lucio', 'mccree',
            'mercy', 'reaper', 'reinhardt', 'roadhog', 'soldier-76',
            'torbjorn', 'tracer', 'widowmaker', 'zarya', 'zenyatta']

  def __init__(self, original):
    self.red_team = set()
    self.blue_team = set()
    self.original = original
    self.thickness = 2
    self.color = (255, 0, 0)
    self.hero_detector = HeroDetector(self.original)

  def detect(self):
    self.hero_detector.draw_divider()

    for hero in self.__class__.heroes:
      path = os.path.abspath('src/heroes/' + hero + '.png')
      template = cv2.imread(path, 0)
      w, h = template.shape[::-1]
      points = self.hero_detector.detect(template)

      for point1 in points:
        if self.hero_detector.is_red_team(point1[1]):
          self.red_team.add(hero)
        else:
          self.blue_team.add(hero)
        point2 = (point1[0] + w, point1[1] + h)
        cv2.rectangle(self.original, point1, point2, self.color, self.thickness)
