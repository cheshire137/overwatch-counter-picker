import unittest
from src.hero_picker import HeroPicker

class HeroPickerTest(unittest.TestCase):
  def test_suggests_counter_healer(self):
    red_team = ['mercy', 'lucio', 'dva', 'genji', 'tracer', 'reinhardt']
    blue_team = ['dva', 'genji', 'hanzo', 'widowmaker', 'mccree']
    hero_picker = HeroPicker(red_team, blue_team)
    self.assertEqual(['lucio'], hero_picker.pick())

  def test_suggests_counter_tank(self):
    red_team = ['hanzo', 'lucio', 'reaper', 'genji', 'tracer', 'reinhardt']
    blue_team = ['mercy', 'genji', 'hanzo', 'widowmaker', 'mccree']
    hero_picker = HeroPicker(red_team, blue_team)
    self.assertEqual(['dva'], hero_picker.pick())

  def test_suggests_counter_offense(self):
    red_team = ['hanzo', 'lucio', 'reaper', 'genji', 'mei', 'reinhardt']
    blue_team = ['mercy', 'reinhardt', 'hanzo', 'widowmaker', 'bastion']
    hero_picker = HeroPicker(red_team, blue_team)
    self.assertEqual(['pharah', 'reaper'], hero_picker.pick())

  def test_suggests_healer(self):
    red_team = []
    blue_team = ['dva', 'roadhog', 'reinhardt', 'genji', 'mei']
    hero_picker = HeroPicker(red_team, blue_team)
    self.assertEqual(['mercy', 'ana'], hero_picker.pick())
