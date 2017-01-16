import cv2
import numpy as np
import imutils
import math

SCREENSHOT_WIDTH = 2560

class HeroDetector:
  def __init__(self, original):
    self.original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    (self.original_h, self.original_w) = self.original.shape[:2]

    self.resized = False
    if self.original_w != SCREENSHOT_WIDTH:
      self.resized = True
      self.original = imutils.resize(self.original, width=SCREENSHOT_WIDTH)

    self.mid_height = self.original_h / 2
    self.threshold = 0.8

  # Returns a unique list of tuples with x,y coordinates for the top left of
  # where the given template appears in the original image. Returns None if the
  # template was not detected.
  def detect(self, template):
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(self.original, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= self.threshold)
    points = zip(*loc[::-1])

    if len(points) > 0:
      rounded_points = [(self.round(point[0]), self.round(point[1])) for point in points]
      return list(set(rounded_points))

    return None

  # Returns true if the given y-axis position represents a hero on the red team.
  def is_red_team(self, point):
    return point < self.mid_height

  # Rounds a point so we don't detect the same hero because we matched the template
  # starting at several different-but-very-similar top-left points.
  def round(self, num):
    return int(math.ceil(num / 40.0)) * 40
