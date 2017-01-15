import unittest

from src.models.hero_picker import HeroPicker
from src.models.red_team import RedTeam
from src.models.blue_team import BlueTeam
from src.models.roles import Roles

class HeroPickerTest(unittest.TestCase):
  def test_defending(self):
    hero_picker = HeroPicker(RedTeam([]), BlueTeam([]))
    self.assertFalse(hero_picker.defending())

    hero_picker = HeroPicker(RedTeam([]), BlueTeam([]), attacking=True)
    self.assertFalse(hero_picker.defending())

    hero_picker = HeroPicker(RedTeam([]), BlueTeam([]), attacking=False)
    self.assertTrue(hero_picker.defending())

  def test_suggests_counter_healer(self):
    red_team = RedTeam(['mercy', 'lucio', 'dva', 'genji', 'tracer', 'reinhardt'])
    blue_team = BlueTeam(['dva', 'genji', 'hanzo', 'widowmaker', 'mccree'])
    hero_picker = HeroPicker(red_team, blue_team)
    self.assertEqual(['mercy', 'lucio'], hero_picker.pick())

  def test_suggests_counter_tank(self):
    red_team = RedTeam(['hanzo', 'lucio', 'reaper', 'genji', 'tracer', 'reinhardt'])
    blue_team = BlueTeam(['mercy', 'genji', 'hanzo', 'widowmaker', 'mccree'])
    hero_picker = HeroPicker(red_team, blue_team)
    self.assertEqual(['dva'], hero_picker.pick())

  def test_suggests_counter_offense(self):
    red_team = RedTeam(['hanzo', 'lucio', 'reaper', 'genji', 'mei', 'reinhardt'])
    blue_team = BlueTeam(['mercy', 'reinhardt', 'hanzo', 'widowmaker', 'bastion'])
    hero_picker = HeroPicker(red_team, blue_team)
    self.assertEqual(['pharah'], hero_picker.pick())

  def test_suggests_healer(self):
    red_team = RedTeam([])
    blue_team = BlueTeam(['dva', 'roadhog', 'reinhardt', 'genji', 'mei'])
    hero_picker = HeroPicker(red_team, blue_team)
    self.assertEqual(['mercy'], hero_picker.pick())

  def test_suggests_offense(self):
    red_team = RedTeam([])
    blue_team = BlueTeam(['dva', 'zenyatta', 'mercy', 'roadhog', 'mei'])
    hero_picker = HeroPicker(red_team, blue_team)
    self.assertEqual(['pharah', 'soldier76'], hero_picker.pick())

  def test_suggests_defense_on_defense(self):
    red_team = RedTeam([])
    blue_team = BlueTeam(['pharah', 'mercy', 'roadhog', 'dva', 'soldier76'])
    hero_picker = HeroPicker(red_team, blue_team, attacking=False)
    self.assertTrue(hero_picker.defending(), 'expected to be defending')
    picks = hero_picker.pick()
    self.assertNotEqual(0, len(picks))
    for hero in picks:
      self.assertTrue(hero in Roles.defense, 'expected ' + hero + ' to be a defense hero')

if __name__ == "__main__":
  unittest.main()
