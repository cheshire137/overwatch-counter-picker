import unittest

from src.db.models.team_composition import TeamComposition

class TeamCompositionTest(unittest.TestCase):
  def test_constructor(self):
    team_comp = TeamComposition(sombra=1, dva=2, lucio=1)
    self.assertEqual(1, team_comp.sombra)
    self.assertEqual(2, team_comp.dva)
    self.assertEqual(1, team_comp.lucio)
    self.assertEqual(None, team_comp.soldier76)

  def test_counts_from_list(self):
    counts = TeamComposition.counts_from_list(['ana', 'mercy', 'ana', 'zarya'])
    self.assertEqual({'ana': 2, 'mercy': 1, 'zarya': 1}, counts)

  def test_heroes(self):
    team_comp = TeamComposition(sombra=1, dva=2, lucio=1)
    self.assertEqual(['dva', 'lucio', 'sombra'], team_comp.heroes())

  def test_counts(self):
    team_comp = TeamComposition(sombra=1, dva=2, lucio=1)
    self.assertEqual({'sombra': 1, 'dva': 2, 'lucio': 1}, team_comp.counts())
