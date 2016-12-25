import cv2
import numpy as np
import imutils

class HeroDetector:
  def __init__(self, original):
    self.original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    (self.original_h, self.original_w) = self.original.shape[:2]
    if self.original_w < 2560:
      self.original = imutils.resize(self.original, width=2560)
    self.mid_height = self.original_h / 2
    self.threshold = 0.8

  def detect(self, template):
    res = cv2.matchTemplate(self.original, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= self.threshold)
    return zip(*loc[::-1])

  def is_red_team(self, point):
    return point < self.mid_height
