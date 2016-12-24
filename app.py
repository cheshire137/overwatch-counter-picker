import cv2

original = cv2.imread('sample-screenshots/full-teams.jpg', 0)
template = cv2.imread('heroes/mercy.png', 0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(original, template, cv2.TM_CCORR)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)

print 'Found Mercy at', top_left, 'to', bottom_right
