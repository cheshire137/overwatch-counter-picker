import unittest

from src.models.blue_team import BlueTeam
from src.models.roles import Roles

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

  def test_num_in_role_excludes_player(self):
    team = BlueTeam([])
    team.add('mercy', 300)
    team.add('widowmaker', 130) # player, defense
    team.add('hanzo', 150) # defense
    team.add('symmetra', 314)
    team.add('bastion', 400) # defense
    team.add('roadhog', 392)
    self.assertEqual(2, team.num_in_role(Roles.defense))

  def test_num_in_role_does_not_exclude_anyone_when_not_full(self):
    team = BlueTeam([])
    team.add('mercy', 300)
    team.add('widowmaker', 130) # defense
    team.add('hanzo', 150) # defense
    team.add('symmetra', 314)
    team.add('bastion', 400) # defense
    self.assertEqual(3, team.num_in_role(Roles.defense))

  def test_allies_excludes_player_when_fully_detected(self):
    team = BlueTeam([])
    team.add('mercy', 300)
    team.add('widowmaker', 130) # player
    team.add('hanzo', 150)
    team.add('symmetra', 314)
    team.add('bastion', 400)
    team.add('roadhog', 392)
    expected = ['hanzo', 'mercy', 'symmetra', 'roadhog', 'bastion']
    self.assertEqual(expected, team.allies())

  def test_allies_excludes_unknowns(self):
    team = BlueTeam([])
    team.add('mercy', 300)
    team.add('widowmaker', 130)
    team.add('hanzo', 150)
    team.add('unknown', 314)
    team.add('bastion', 400)
    expected = ['widowmaker', 'hanzo', 'mercy', 'bastion']
    self.assertEqual(expected, team.allies())

if __name__ == '__main__':
  unittest.main()
