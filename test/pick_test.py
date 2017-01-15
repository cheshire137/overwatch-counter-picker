import unittest

from src.db.models.pick import Pick

class PickTest(unittest.TestCase):
  def test_constructor(self):
    pick_attrs = {
      'screenshot_width': 640,
      'screenshot_height': 480,
      'player': 'mercy',
      'blue_team_id': 1,
      'red_team_id': 2
    }
    pick_attrs.update({hero: True for hero in ['mercy', 'zenyatta']})
    pick = Pick(**pick_attrs)
    self.assertEqual(640, pick.screenshot_width)
    self.assertEqual(480, pick.screenshot_height)
    self.assertEqual('mercy', pick.player)
    self.assertEqual(1, pick.blue_team_id)
    self.assertEqual(2, pick.red_team_id)
    self.assertTrue(pick.mercy)
    self.assertTrue(pick.zenyatta)
