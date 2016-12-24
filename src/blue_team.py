from team import Team

class BlueTeam(Team):
  def player(self):
    if not self.fully_detected():
      return None

    return min(self.positions, key=self.positions.get)

  def allies(self):
    player = self.player()
    if player is not None:
      return [hero for hero in self.heroes if hero != player]
    return self.heroes
