import cv2
import numpy as np
import sys

original_name = 'full-teams.jpg'
if len(sys.argv) > 1:
  original_name = sys.argv[1]
  print 'Using screenshot', original_name, '\n'
else:
  print 'You can pass a file name from sample-screenshots/'
  print 'Example:'
  print 'python', sys.argv[0], 'name_of_sample_screenshot_here\n'
  print 'Using default screenshot', original_name, '\n'

class HeroDetector:
  def __init__(self, original):
    self.original = original
    self.original_gray = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)
    self.original_w = np.size(self.original, 1)
    self.original_h = np.size(self.original, 0)
    self.mid_height = self.original_h / 2
    self.threshold = 0.8
    self.thickness = 2
    self.color = (0, 0, 255)

  def draw_divider(self):
    point1 = (0, self.mid_height)
    point2 = (self.original_w, self.mid_height)
    cv2.rectangle(self.original, point1, point2, self.color, self.thickness)

  def detect(self, template):
    res = cv2.matchTemplate(self.original_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= self.threshold)
    return zip(*loc[::-1])

  def is_red_team(self, point):
    return point < self.mid_height

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
      template = cv2.imread('heroes/' + hero + '.png', 0)
      w, h = template.shape[::-1]
      points = self.hero_detector.detect(template)

      for point1 in points:
        if self.hero_detector.is_red_team(point1[1]):
          self.red_team.add(hero)
        else:
          self.blue_team.add(hero)
        point2 = (point1[0] + w, point1[1] + h)
        cv2.rectangle(self.original, point1, point2, self.color, self.thickness)

thickness = 2
blue = (255, 0, 0)
red = (0, 0, 255)

original = cv2.imread('sample-screenshots/' + original_name)
team_detector = TeamDetector(original)
team_detector.detect()

print 'Red team:', team_detector.red_team
print 'Blue team:', team_detector.blue_team

output_path = 'res.png'
cv2.imwrite(output_path, original)
print '\nLook at', output_path, 'to see Overwatch hero detection'
