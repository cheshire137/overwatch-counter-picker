import unittest
from src.team import Team

class TeamTest(unittest.TestCase):
  def test_num_healers(self):
    team = Team(['ana', 'dva', 'reinhardt'])
    self.assertEqual(1, team.num_healers())

    team = Team(['widowmaker', 'mercy', 'zenyatta', 'symmetra'])
    self.assertEqual(2, team.num_healers())

  def test_num_defense(self):
    team = Team(['ana', 'dva', 'reinhardt'])
    self.assertEqual(0, team.num_defense())

    team = Team(['widowmaker', 'mercy', 'zenyatta', 'symmetra'])
    self.assertEqual(1, team.num_defense())

  def test_num_offense(self):
    team = Team(['ana', 'dva', 'reinhardt'])
    self.assertEqual(0, team.num_offense())

    team = Team(['torbjorn', 'mercy', 'lucio', 'soldier-76'])
    self.assertEqual(1, team.num_offense())

  def test_num_tanks(self):
    team = Team(['ana', 'dva', 'reinhardt'])
    self.assertEqual(2, team.num_tanks())

    team = Team(['torbjorn', 'mercy', 'lucio', 'soldier-76'])
    self.assertEqual(0, team.num_tanks())

  def test_size(self):
    team = Team(['ana', 'dva', 'reinhardt'])
    self.assertEqual(3, team.size())

    team = Team(['ana', 'unknown', 'reinhardt'])
    self.assertEqual(2, team.size())

  def test_fully_detected(self):
    team = Team(['ana', 'dva', 'reinhardt'])
    self.assertFalse(team.fully_detected())

    team = Team(['ana', 'dva', 'reinhardt', 'unknown', 'unknown', 'hanzo'])
    self.assertTrue(team.fully_detected())

  def test_add_adds_heroes(self):
    team = Team([])
    self.assertEqual([], team.heroes)
    team.add('mercy', 1)
    self.assertEqual(['mercy'], team.heroes)

  def test_add_orders_heroes_by_position(self):
    team = Team([])
    team.add('mercy', 1)
    team.add('ana', 0)
    team.add('reinhardt', 2)
    self.assertEqual(['ana', 'mercy', 'reinhardt'], team.heroes)

  def test_add_allows_multiple_unknowns(self):
    team = Team([])
    team.add('unknown', 0)
    team.add('lucio', 1)
    team.add('unknown', 2)
    self.assertEqual(['unknown', 'lucio', 'unknown'], team.heroes)

  def test_add_disallows_duplicate_heroes(self):
    team = Team([])
    team.add('unknown', 0)
    team.add('lucio', 1)
    team.add('lucio', 2)
    self.assertEqual(['unknown', 'lucio'], team.heroes)
