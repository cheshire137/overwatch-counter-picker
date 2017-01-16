import unittest
import cv2

from src.models.hero_detector import HeroDetector

class HeroDetectorTest(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.full_teams = cv2.imread('sample-screenshots/full-teams.jpg')
    cls.fire_and_death = cv2.imread('sample-screenshots/fire-and-death.jpg')
    cls.eichenwalde_full = cv2.imread('sample-screenshots/eichenwalde-full.jpg')
    cls.cards_screen = cv2.imread('sample-screenshots/cards-screen.jpg')
    cls.cards_screen2 = cv2.imread('sample-screenshots/cards-screen2.jpg')

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
    template = cv2.imread('src/templates/ana.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertTrue(detector.is_red_team(points[0][1]), 'should be on red team')

  def test_detect_finds_ana_on_cards_screen(self):
    detector = HeroDetector(self.__class__.cards_screen)
    template = cv2.imread('src/templates/ana.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertTrue(detector.is_red_team(points[0][1]), 'should be on red team')

    detector = HeroDetector(self.__class__.cards_screen2)
    template = cv2.imread('src/templates/ana.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertTrue(detector.is_red_team(points[0][1]), 'should be on red team')

  def test_detect_finds_winston_when_present(self):
    detector = HeroDetector(self.__class__.fire_and_death)
    template = cv2.imread('src/templates/winston.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertTrue(detector.is_red_team(points[0][1]), 'should be on red team')

  def test_detect_finds_pharah_when_present(self):
    detector = HeroDetector(self.__class__.fire_and_death)
    template = cv2.imread('src/templates/pharah.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertTrue(detector.is_red_team(points[0][1]), 'should be on red team')

  def test_detect_finds_pharah_on_cards_screen(self):
    detector = HeroDetector(self.__class__.cards_screen2)
    template = cv2.imread('src/templates/pharah.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    red_pharah = points[0]
    blue_pharah = points[1]
    self.assertTrue(detector.is_red_team(red_pharah[1]), 'should be on red team')
    self.assertFalse(detector.is_red_team(blue_pharah[1]), 'should be on blue team')

  def test_detect_finds_mercy_when_present(self):
    detector = HeroDetector(self.__class__.fire_and_death)
    template = cv2.imread('src/templates/mercy.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_mercy_on_cards_screen(self):
    detector = HeroDetector(self.__class__.cards_screen)
    template = cv2.imread('src/templates/mercy.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_symmetra_when_present(self):
    detector = HeroDetector(self.__class__.fire_and_death)
    template = cv2.imread('src/templates/symmetra.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_sombra_when_present(self):
    detector = HeroDetector(self.__class__.fire_and_death)
    template = cv2.imread('src/templates/sombra.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_tracer_when_present(self):
    detector = HeroDetector(self.__class__.fire_and_death)
    template = cv2.imread('src/templates/tracer.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_tracer_on_cards_screen(self):
    detector = HeroDetector(self.__class__.cards_screen)
    template = cv2.imread('src/templates/tracer.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_soldier_76_when_present(self):
    detector = HeroDetector(self.__class__.fire_and_death)
    template = cv2.imread('src/templates/soldier76.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_soldier_76_on_cards_screen(self):
    detector = HeroDetector(self.__class__.cards_screen)
    template = cv2.imread('src/templates/soldier76.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_roadhog_when_present(self):
    detector = HeroDetector(self.__class__.fire_and_death)
    template = cv2.imread('src/templates/roadhog.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_roadhog_on_cards_screen(self):
    detector = HeroDetector(self.__class__.cards_screen2)
    template = cv2.imread('src/templates/roadhog.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_reinhardt_on_cards_screen(self):
    detector = HeroDetector(self.__class__.cards_screen2)
    template = cv2.imread('src/templates/reinhardt.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertTrue(detector.is_red_team(points[0][1]), 'should be on red team')

  def test_detect_finds_reaper_when_present(self):
    detector = HeroDetector(self.__class__.full_teams)
    template = cv2.imread('src/templates/reaper.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_reaper_on_cards_screen(self):
    detector = HeroDetector(self.__class__.cards_screen2)
    template = cv2.imread('src/templates/reaper.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_zenyatta_when_present(self):
    detector = HeroDetector(self.__class__.full_teams)
    template = cv2.imread('src/templates/zenyatta.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_zenyatta_on_cards_screen(self):
    detector = HeroDetector(self.__class__.cards_screen)
    template = cv2.imread('src/templates/zenyatta.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    red_zenyatta = points[0]
    blue_zenyatta = points[1]
    self.assertTrue(detector.is_red_team(red_zenyatta[1]), 'should be on red team')
    self.assertFalse(detector.is_red_team(blue_zenyatta[1]), 'should be on blue team')

  def test_detect_finds_zarya_when_present(self):
    detector = HeroDetector(self.__class__.full_teams)
    template = cv2.imread('src/templates/zarya.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_zarya_on_cards_screen(self):
    detector = HeroDetector(self.__class__.cards_screen)
    template = cv2.imread('src/templates/zarya.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertTrue(detector.is_red_team(points[0][1]), 'should be on red team')

  def test_detect_finds_genji_when_present(self):
    detector = HeroDetector(self.__class__.full_teams)
    template = cv2.imread('src/templates/genji.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertTrue(detector.is_red_team(points[0][1]), 'should be on red team')

  def test_detect_finds_genji_on_cards_screen(self):
    detector = HeroDetector(self.__class__.cards_screen)
    template = cv2.imread('src/templates/genji.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertTrue(detector.is_red_team(points[0][1]), 'should be on red team')

  def test_detect_finds_lucio_when_present(self):
    detector = HeroDetector(self.__class__.full_teams)
    template = cv2.imread('src/templates/lucio.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertTrue(detector.is_red_team(points[0][1]), 'should be on red team')

  def test_detect_finds_mei_when_present(self):
    detector = HeroDetector(self.__class__.eichenwalde_full)
    template = cv2.imread('src/templates/mei.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_mei_on_cards_screen(self):
    detector = HeroDetector(self.__class__.cards_screen)
    template = cv2.imread('src/templates/mei.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertTrue(detector.is_red_team(points[0][1]), 'should be on red team')

  def test_detect_finds_widowmaker_on_cards_screen(self):
    detector = HeroDetector(self.__class__.cards_screen)
    template = cv2.imread('src/templates/widowmaker.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertTrue(detector.is_red_team(points[0][1]), 'should be on red team')

  def test_detect_finds_junkrat_on_cards_screen(self):
    detector = HeroDetector(self.__class__.cards_screen)
    template = cv2.imread('src/templates/junkrat.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_dva_on_cards_screen(self):
    detector = HeroDetector(self.__class__.cards_screen)
    template = cv2.imread('src/templates/dva.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_detect_finds_same_hero_on_each_team(self):
    detector = HeroDetector(self.__class__.full_teams)
    template = cv2.imread('src/templates/dva.png')
    points = detector.detect(template)
    self.assertEqual(2, len(points))
    self.assertNotEqual(points[0][1], points[1][1], \
                        'D.Va should be found once on each team')

  def test_detect_finds_hanzo_on_cards_screen(self):
    detector = HeroDetector(self.__class__.cards_screen2)
    template = cv2.imread('src/templates/hanzo.png')
    points = detector.detect(template)
    self.assertTrue(points, 'points should not be None')
    self.assertFalse(detector.is_red_team(points[0][1]), 'should be on blue team')

  def test_combine_points(self):
    points = [(1637, 357), (1638, 357), (1636, 358), (1637, 358), (1638, 358), \
      (1639, 358), (1640, 358), (1636, 359), (1637, 359), (1638, 359), \
      (1639, 359), (1640, 359), (1637, 360), (1638, 360), (1639, 360), \
      (1640, 360), (1636, 764), (1637, 764), (1638, 764), (1639, 764), \
      (1636, 765), (1637, 765), (1638, 765), (1639, 765), (1640, 765), \
      (1636, 766), (1637, 766), (1638, 766), (1639, 766), (1640, 766), \
      (1638, 767), (1639, 767)]
    expected = [(1630, 760), (1630, 350)]
    actual = HeroDetector.combine_points(points)
    self.assertEqual(expected, actual)

  def test_detect_if_cards_screen(self):
    detector = HeroDetector(self.__class__.cards_screen)
    self.assertTrue(detector.is_cards_screen)

    detector = HeroDetector(self.__class__.full_teams)
    self.assertFalse(detector.is_cards_screen)

if __name__ == '__main__':
  unittest.main()
