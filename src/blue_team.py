from team import Team

class BlueTeam(Team):
  def player(self):
    if not self.full():
      return None

    return min(self.positions, key=self.positions.get)
