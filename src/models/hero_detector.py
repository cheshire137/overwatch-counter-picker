import cv2
import numpy as np
import imutils
import math

class HeroDetector:
  def __init__(self, original):
    self.original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    (self.original_h, self.original_w) = self.original.shape[:2]
    if self.original_w != 2560:
      self.original = imutils.resize(self.original, width=2560)
    self.mid_height = self.original_h / 2
    self.threshold = 0.8

  # Returns a list of tuples with x,y coordinates for the top left of where the
  # given template appears in the original image. Returns None if the template
  # was not detected.
  def detect(self, template):
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(self.original, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= self.threshold)
    points = zip(*loc[::-1])
    if len(points) > 0:
      rounded_points = [(self.round(point[0]), self.round(point[1])) for point in points]
      return list(set(rounded_points))
    return None

  # Returns true if the given y-axis position represents a hero on the red team.
  def is_red_team(self, point):
    return point < self.mid_height

  def round(self, num):
    return int(math.ceil(num / 40.0)) * 40
