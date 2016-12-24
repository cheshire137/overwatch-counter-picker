import cv2
import numpy as np

original = cv2.imread('sample-screenshots/full-teams.jpg')
original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

heroes = ['dva', 'genji', 'lucio', 'mercy', 'reaper', 'reinhardt',
          'roadhog', 'tracer', 'zarya', 'zenyatta']

for hero in heroes:
  print 'Detecting', hero + '...'
  template = cv2.imread('heroes/' + hero + '.png', 0)
  w, h = template.shape[::-1]

  res = cv2.matchTemplate(original_gray, template, cv2.TM_CCOEFF_NORMED)

  threshold = 0.8
  loc = np.where(res >= threshold)

  thickness = 2
  color = (0, 0, 255)

  for pt in zip(*loc[::-1]):
    point1 = pt
    point2 = (pt[0] + w, pt[1] + h)
    cv2.rectangle(original, point1, point2, color, thickness)

output_path = 'res.png'
cv2.imwrite(output_path, original)
print 'Look at', output_path, 'to see Overwatch hero detection'
