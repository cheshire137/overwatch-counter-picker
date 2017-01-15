import unittest

from src.db.models.team_composition import TeamComposition

class TeamCompositionTest(unittest.TestCase):
  def test_constructor(self):
    team_comp = TeamComposition(sombra=1, dva=2, lucio=1)
    self.assertEqual(1, team_comp.sombra)
    self.assertEqual(2, team_comp.dva)
    self.assertEqual(1, team_comp.lucio)
    self.assertEqual(None, team_comp.soldier76)

  def test_from_list(self):
    team_comp = TeamComposition.from_list(['ana', 'mercy', 'ana', 'zarya'])
    self.assertEqual(2, team_comp.ana)
    self.assertEqual(1, team_comp.mercy)
    self.assertEqual(1, team_comp.zarya)
    self.assertEqual(None, team_comp.reaper)
