import cv2
import numpy as np

original = cv2.imread('sample-screenshots/full-teams.jpg')
original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

template = cv2.imread('heroes/mercy.png', 0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(original_gray, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where(res >= threshold)
for pt in zip(*loc[::-1]):
  cv2.rectangle(original, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
cv2.imwrite('res.png', original)

print 'Look at res.png to see Mercy detection'
