import cv2
import numpy as np
import sys

original_name = 'full-teams.jpg'
if len(sys.argv) > 1:
  original_name = sys.argv[1]
  print 'Using screenshot', original_name
else:
  print 'You can pass a file name from sample-screenshots/'
  print 'Example:'
  print 'python', sys.argv[0], 'name_of_sample_screenshot_here\n'
  print 'Using default screenshot', original_name

class HeroDetector:
  def __init__(self, original):
    self.original = original
    self.original_gray = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)
    self.original_w = np.size(self.original, 1)
    self.original_h = np.size(self.original, 0)
    self.mid_height = self.original_h / 2
    self.threshold = 0.8

  def detect(self, template):
    res = cv2.matchTemplate(self.original_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= self.threshold)
    return zip(*loc[::-1])

original = cv2.imread('sample-screenshots/' + original_name)
detector = HeroDetector(original)

# TODO: symmetra, hanzo, sombra, pharah, mei, winston
heroes = ['ana', 'bastion', 'dva', 'genji', 'junkrat', 'lucio', 'mccree',
          'mercy', 'reaper', 'reinhardt', 'roadhog', 'soldier-76',
          'torbjorn', 'tracer', 'widowmaker', 'zarya', 'zenyatta']

thickness = 2
blue = (255, 0, 0)
red = (0, 0, 255)

print 'Screenshot is', detector.original_w, 'x', detector.original_h
print 'Vertical midpoint is', detector.mid_height, '\n'
cv2.rectangle(original, (0, detector.mid_height), (detector.original_w, detector.mid_height), blue, 2)

blue_team = set()
red_team = set()

for hero in heroes:
  print 'Detecting', hero + '...'
  template = cv2.imread('heroes/' + hero + '.png', 0)
  w, h = template.shape[::-1]
  points = detector.detect(template)

  if len(points) > 0:
    print '\tfound'

  for point1 in points:
    if point1[1] < detector.mid_height:
      red_team.add(hero)
    else:
      blue_team.add(hero)
    point2 = (point1[0] + w, point1[1] + h)
    cv2.rectangle(original, point1, point2, red, thickness)

print '\nBlue team:', blue_team
print 'Red team:', red_team

output_path = 'res.png'
cv2.imwrite(output_path, original)
print '\nLook at', output_path, 'to see Overwatch hero detection'
