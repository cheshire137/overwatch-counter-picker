import unittest
import cv2

from src.models.team_detector import TeamDetector

class TeamDetectorTest(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.smaller_screenshot = cv2.imread('sample-screenshots/smaller-screenshot.jpg')
    cls.cards_screen = cv2.imread('sample-screenshots/cards-screen.jpg')

  def test_detect_populates_teams(self):
    detector = TeamDetector(self.__class__.smaller_screenshot)
    self.assertEqual([], detector.red_team.heroes)
    self.assertEqual([], detector.blue_team.heroes)
    detector.detect()
    self.assertEqual(['mccree', 'ana', 'zarya', 'dva', 'widowmaker', \
                      'zenyatta'], detector.red_team.heroes)
    self.assertEqual(['zenyatta', 'mercy', 'dva', 'soldier76', 'torbjorn', \
                      'reinhardt'], detector.blue_team.heroes)

  def test_detects_heroes_on_cards_screen(self):
    detector = TeamDetector(self.__class__.cards_screen)
    detector.detect()

    red_team = ['zarya', 'genji', 'mei', 'widowmaker', 'ana', 'zenyatta']
    self.assertEqual(red_team, detector.red_team.heroes)

    blue_team = ['mercy', 'zenyatta', 'soldier76', 'junkrat', 'dva', 'tracer']
    self.assertEqual(blue_team, detector.blue_team.heroes)

if __name__ == '__main__':
  unittest.main()
