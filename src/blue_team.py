from team import Team

class BlueTeam(Team):
  def player(self):
    return min(self.positions, key=self.positions.get)
