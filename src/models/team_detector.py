import cv2
import os

from src.models.hero_detector import HeroDetector
from src.models.red_team import RedTeam
from src.models.blue_team import BlueTeam

class TeamDetector:
  heroes = ['ana', 'bastion', 'dva', 'genji', 'hanzo', 'junkrat', 'lucio',
            'mccree', 'mei', 'mercy', 'pharah', 'reaper', 'reinhardt',
            'roadhog', 'soldier76', 'sombra', 'symmetra', 'torbjorn', 'tracer',
            'widowmaker', 'winston', 'zarya', 'zenyatta', 'unknown']

  def __init__(self, original):
    self.red_team = RedTeam([])
    self.blue_team = BlueTeam([])
    self.thickness = 2
    self.color = (255, 0, 0)
    self.hero_detector = HeroDetector(original)
    self.seen_positions = []

  # Look in the original image for each Overwatch hero.
  def detect(self, draw_boxes=False):
    for hero in self.__class__.heroes:
      self.detect_hero(hero, draw_boxes=draw_boxes)

  # Returns an image template for finding the given hero within a larger image.
  def get_hero_template(self, hero):
    path = os.path.abspath('src/templates/' + hero + '.png')
    return cv2.imread(path)

  # Look for the given hero in the original image.
  def detect_hero(self, hero, draw_boxes=False):
    template = self.get_hero_template(hero)
    (height, width) = template.shape[:2]
    points = self.hero_detector.detect(template)

    if points is None:
      return

    valid_points = [point for point in points if self.valid_position(point)]
    for top_left_point in valid_points:
      if self.have_seen_position(top_left_point):
        return

      self.add_hero_to_team(hero, top_left_point)

      if draw_boxes:
        bottom_right_point = (top_left_point[0] + width, top_left_point[1] + height)
        cv2.rectangle(self.hero_detector.original, top_left_point, \
                      bottom_right_point, self.color, self.thickness)

  # Adds the given hero to the appropriate team based on the given point that is
  # the top-left point where the hero's template was found in the larger image.
  def add_hero_to_team(self, hero, top_left_point):
    (x, y) = top_left_point
    if self.hero_detector.is_red_team(y):
      self.red_team.add(hero, x)
    else:
      self.blue_team.add(hero, x)

  def have_seen_position(self, point):
    if point in self.seen_positions:
      return True

    self.seen_positions.append(point)
    return False

  # Returns true if the given point represents a valid location where we expect
  # a hero portrait to be in the team composition screen.
  def valid_position(self, point):
    # Needs to be beyond 500px from the left in a 2560x1440 screenshot.
    return point[0] > 500
