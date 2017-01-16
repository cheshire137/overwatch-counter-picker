import cv2
import os
import numpy as np
import imutils
import math

TARGET_WIDTH = 2560

class HeroDetector:
  def __init__(self, original, is_cards_screen=False):
    self.original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    (self.original_h, self.original_w) = self.original.shape[:2]
    self.threshold = 0.8
    self.is_cards_screen = False
    self.resized_w = self.original_w
    self.resized_h = self.original_h

    if self.original_w != TARGET_WIDTH:
      self.original = imutils.resize(self.original, width=TARGET_WIDTH)
      (self.resized_h, self.resized_w) = self.original.shape[:2]

    self.mid_height = int(self.resized_h / 2.0)

    # Now can detect if we're on the game-over screen with voting cards, since
    # we've scaled the image to the same size from which the 'rate match'
    # template was taken.
    self.is_cards_screen = self.detect_if_cards_screen()

  # Returns a unique list of tuples with x,y coordinates for the top left of
  # where the given template appears in the original image. Returns None if the
  # template was not detected.
  def detect(self, template):
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    if self.is_cards_screen:
      template = self.scale_template_for_cards_screen(template)

    result = cv2.matchTemplate(self.original, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= self.threshold)
    points = zip(*loc[::-1])

    if len(points) > 0:
      return HeroDetector.combine_points(points)

    return None

  # Scale template down if we're on the game-over screen since the hero
  # portraits are smaller there than during the game.
  def scale_template_for_cards_screen(self, template):
    (height, width) = template.shape[:2]
    new_width = int(math.ceil(width * 0.79))
    return imutils.resize(template, width=new_width)

  # Returns true if the given y-axis position represents a hero on the red team.
  def is_red_team(self, point):
    return point < self.mid_height

  # Given a list of points where a particular hero was detected in the larger
  # image, this will combine the points that are close enough together that they
  # must be detecting the same hero.
  @classmethod
  def combine_points(cls, points):
    rounded_points = [(cls.round(point[0]), cls.round(point[1])) for point in points]
    unique_points = list(set(rounded_points))

    x_filter = lambda p, point: p[1] == point[1] and abs(point[0] - p[0]) <= 40
    combined_points = cls.combine_similar_points(unique_points, x_filter)

    y_filter = lambda p, point: p[0] == point[0] and abs(point[1] - p[1]) <= 40
    combined_points = cls.combine_similar_points(combined_points, y_filter)

    return combined_points

  # Given a list of points and a lambda filter function, this will return a subset
  # of those points after using the filter to find similar points and average
  # them together.
  @classmethod
  def combine_similar_points(cls, points, filterer):
    result = []

    for point in points:
      similar_points = filter(lambda p: p != point and filterer(p, point), points)

      if len(similar_points) < 1:
        result.append(point)
        continue

      similar_point = similar_points[0]
      avg_x = int((point[0] + similar_point[0]) / 2.0)
      avg_y = int((point[1] + similar_point[1]) / 2.0)

      avg_point = (avg_x, avg_y)
      if not avg_point in result:
        result.append(avg_point)

    return result

  # Returns True if the screenshot is of the game-over screen where hero cards
  # are shown.
  def detect_if_cards_screen(self):
    path = os.path.abspath('src/templates/rate-match.png')
    template = cv2.imread(path)
    points = self.detect(template)
    return points is not None

  # Rounds a point so we don't detect the same hero because we matched the template
  # starting at several different-but-very-similar top-left points.
  @classmethod
  def round(cls, num):
    return int(math.floor(num / 20.0)) * 20
