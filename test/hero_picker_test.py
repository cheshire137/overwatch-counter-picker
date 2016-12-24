import unittest
from src.hero_picker import HeroPicker
from src.team import Team

class HeroPickerTest(unittest.TestCase):
  def test_defending(self):
    hero_picker = HeroPicker(Team([]), Team([]))
    self.assertFalse(hero_picker.defending())

    hero_picker = HeroPicker(Team([]), Team([]), attacking=True)
    self.assertFalse(hero_picker.defending())

    hero_picker = HeroPicker(Team([]), Team([]), attacking=False)
    self.assertTrue(hero_picker.defending())

  def test_suggests_counter_healer(self):
    red_team = Team(['mercy', 'lucio', 'dva', 'genji', 'tracer', 'reinhardt'])
    blue_team = Team(['dva', 'genji', 'hanzo', 'widowmaker', 'mccree'])
    hero_picker = HeroPicker(red_team, blue_team)
    self.assertEqual(['mercy', 'lucio'], hero_picker.pick())

  def test_suggests_counter_tank(self):
    red_team = Team(['hanzo', 'lucio', 'reaper', 'genji', 'tracer', 'reinhardt'])
    blue_team = Team(['mercy', 'genji', 'hanzo', 'widowmaker', 'mccree'])
    hero_picker = HeroPicker(red_team, blue_team)
    self.assertEqual(['dva'], hero_picker.pick())

  def test_suggests_counter_offense(self):
    red_team = Team(['hanzo', 'lucio', 'reaper', 'genji', 'mei', 'reinhardt'])
    blue_team = Team(['mercy', 'reinhardt', 'hanzo', 'widowmaker', 'bastion'])
    hero_picker = HeroPicker(red_team, blue_team)
    self.assertEqual(['pharah'], hero_picker.pick())

  def test_suggests_healer(self):
    red_team = Team([])
    blue_team = Team(['dva', 'roadhog', 'reinhardt', 'genji', 'mei'])
    hero_picker = HeroPicker(red_team, blue_team)
    self.assertEqual(['mercy'], hero_picker.pick())

  def test_suggests_defense_on_defense(self):
    red_team = Team([])
    blue_team = Team(['genji', 'mercy', 'roadhog', 'zenyatta', 'dva'])
    hero_picker = HeroPicker(red_team, blue_team)
    print hero_picker.pick()
    # self.assertEqual(['mercy'], hero_picker.pick())

if __name__ == "__main__":
  unittest.main()
