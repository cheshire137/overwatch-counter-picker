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

original = cv2.imread('sample-screenshots/' + original_name)
original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

# TODO: symmetra, hanzo, sombra, pharah, mei, winston
heroes = ['ana', 'bastion', 'dva', 'genji', 'junkrat', 'lucio', 'mccree',
          'mercy', 'reaper', 'reinhardt', 'roadhog', 'soldier-76',
          'torbjorn', 'tracer', 'widowmaker', 'zarya', 'zenyatta']

original_w = np.size(original, 1)
original_h = np.size(original, 0)
print 'Screenshot is', original_w, 'x', original_h
mid_height = original_h / 2
print 'Vertical midpoint is', mid_height, '\n'
cv2.rectangle(original, (0, mid_height), (original_w, mid_height), (255, 0, 0), 2)

blue_team = set()
red_team = set()

for hero in heroes:
  print 'Detecting', hero + '...'
  template = cv2.imread('heroes/' + hero + '.png', 0)
  w, h = template.shape[::-1]

  res = cv2.matchTemplate(original_gray, template, cv2.TM_CCOEFF_NORMED)

  threshold = 0.8
  loc = np.where(res >= threshold)

  thickness = 2
  color = (0, 0, 255)

  points = zip(*loc[::-1])
  if len(points) > 0:
    print '\tfound'

  for point1 in points:
    if point1[1] < mid_height:
      red_team.add(hero)
    else:
      blue_team.add(hero)
    point2 = (point1[0] + w, point1[1] + h)
    cv2.rectangle(original, point1, point2, color, thickness)

print '\nBlue team:', blue_team
print 'Red team:', red_team

output_path = 'res.png'
cv2.imwrite(output_path, original)
print '\nLook at', output_path, 'to see Overwatch hero detection'
