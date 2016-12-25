import unittest

from src.models.red_team import RedTeam

class RedTeamTest(unittest.TestCase):
  def test_player_returns_none(self):
    team = RedTeam([])
    self.assertEqual(None, team.player())

    team = RedTeam([])
    team.add('mercy', 300)
    team.add('widowmaker', 130)
    team.add('hanzo', 150)
    team.add('symmetra', 314)
    team.add('bastion', 400)
    team.add('roadhog', 392)
    self.assertEqual(None, team.player())

if __name__ == '__main__':
  unittest.main()
