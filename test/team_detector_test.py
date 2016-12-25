import unittest
import cv2

from src.models.team_detector import TeamDetector

class TeamDetectorTest(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.smaller_screenshot = cv2.imread('sample-screenshots/smaller-screenshot.jpg')

  def test_detect_populates_teams(self):
    detector = TeamDetector(self.__class__.smaller_screenshot)
    self.assertEqual([], detector.red_team.heroes)
    self.assertEqual([], detector.blue_team.heroes)
    detector.detect()
    self.assertEqual(['mccree', 'ana', 'zarya', 'dva', 'widowmaker', \
                      'zenyatta'], detector.red_team.heroes)
    self.assertEqual(['zenyatta', 'mercy', 'dva', 'soldier-76', 'torbjorn', \
                      'reinhardt'], detector.blue_team.heroes)

if __name__ == '__main__':
  unittest.main()
