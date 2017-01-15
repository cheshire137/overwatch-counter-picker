import unittest
import cv2

from src.models.hero_detector import HeroDetector

class HeroDetectorTest(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.full_teams = cv2.imread('sample-screenshots/full-teams.jpg')
    cls.fire_and_death = cv2.imread('sample-screenshots/fire-and-death.jpg')
    cls.eichenwalde_full = cv2.imread('sample-screenshots/eichenwalde-full.jpg')

  def test_constructor_detects_dimensions(self):
    detector = HeroDetector(self.__class__.full_teams)
    self.assertEqual(2560, detector.original_w)
    self.assertEqual(1440, detector.original_h)
    self.assertEqual(720, detector.mid_height)

  def test_is_red_team(self):
    detector = HeroDetector(self.__class__.full_teams)
    self.assertTrue(detector.is_red_team(400))
    self.assertFalse(detector.is_red_team(900))

  def test_detect_finds_ana_when_present(self):
    detector = HeroDetector(self.__class__.fire_and_death)
    template = cv2.imread('src/heroes/ana.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertTrue(detector.is_red_team(points[0][1]), 'should be on red team')

  def test_detect_finds_winston_when_present(self):
    detector = HeroDetector(self.__class__.fire_and_death)
    template = cv2.imread('src/heroes/winston.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertTrue(detector.is_red_team(points[0][1]), 'should be on red team')

  def test_detect_finds_pharah_when_present(self):
    detector = HeroDetector(self.__class__.fire_and_death)
    template = cv2.imread('src/heroes/pharah.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertTrue(detector.is_red_team(points[0][1]), 'should be on red team')

  def test_detect_finds_mercy_when_present(self):
    detector = HeroDetector(self.__class__.fire_and_death)
    template = cv2.imread('src/heroes/mercy.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_symmetra_when_present(self):
    detector = HeroDetector(self.__class__.fire_and_death)
    template = cv2.imread('src/heroes/symmetra.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_sombra_when_present(self):
    detector = HeroDetector(self.__class__.fire_and_death)
    template = cv2.imread('src/heroes/sombra.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_tracer_when_present(self):
    detector = HeroDetector(self.__class__.fire_and_death)
    template = cv2.imread('src/heroes/tracer.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_soldier_76_when_present(self):
    detector = HeroDetector(self.__class__.fire_and_death)
    template = cv2.imread('src/heroes/soldier76.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_roadhog_when_present(self):
    detector = HeroDetector(self.__class__.fire_and_death)
    template = cv2.imread('src/heroes/roadhog.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_reaper_when_present(self):
    detector = HeroDetector(self.__class__.full_teams)
    template = cv2.imread('src/heroes/reaper.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_zenyatta_when_present(self):
    detector = HeroDetector(self.__class__.full_teams)
    template = cv2.imread('src/heroes/zenyatta.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_zarya_when_present(self):
    detector = HeroDetector(self.__class__.full_teams)
    template = cv2.imread('src/heroes/zarya.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_genji_when_present(self):
    detector = HeroDetector(self.__class__.full_teams)
    template = cv2.imread('src/heroes/genji.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertTrue(detector.is_red_team(points[0][1]), 'should be on red team')

  def test_detect_finds_lucio_when_present(self):
    detector = HeroDetector(self.__class__.full_teams)
    template = cv2.imread('src/heroes/lucio.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertTrue(detector.is_red_team(points[0][1]), 'should be on red team')

  def test_detect_finds_mei_when_present(self):
    detector = HeroDetector(self.__class__.eichenwalde_full)
    template = cv2.imread('src/heroes/mei.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_same_hero_on_each_team(self):
    detector = HeroDetector(self.__class__.full_teams)
    template = cv2.imread('src/heroes/dva.png')
    points = detector.detect(template)
    self.assertEqual(2, len(points))
    self.assertNotEqual(points[0][1], points[1][1], \
                        'D.Va should be found once on each team')

if __name__ == '__main__':
  unittest.main()
