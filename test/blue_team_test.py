import unittest
from src.blue_team import BlueTeam

class BlueTeamTest(unittest.TestCase):
  def test_player_returns_none_when_not_fully_detected(self):
    team = BlueTeam([])
    self.assertEqual(None, team.player())

    team = BlueTeam(['unknown'])
    self.assertEqual(None, team.player())

    team = BlueTeam(['hanzo', 'dva', 'reinhardt', 'lucio', 'bastion'])
    self.assertEqual(None, team.player())

  def test_player_returns_leftmost_hero(self):
    team = BlueTeam([])
    team.add('mercy', 300)
    team.add('widowmaker', 130)
    team.add('hanzo', 150)
    team.add('symmetra', 314)
    team.add('bastion', 400)
    team.add('roadhog', 392)
    self.assertEqual('widowmaker', team.player())
