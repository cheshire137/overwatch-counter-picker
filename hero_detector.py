import cv2
import numpy as np

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
