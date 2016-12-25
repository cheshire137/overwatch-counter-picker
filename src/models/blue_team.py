from src.models.team import Team

class BlueTeam(Team):
  def player(self):
    if not self.fully_detected():
      return None
    return self.heroes[0]

  def num_in_role(self, pool):
    count = 0
    player = self.player()
    valid_heroes = [hero for hero in self.heroes if hero != 'unknown' and hero != player]
    for hero in pool:
      if hero in valid_heroes:
        count += 1
    return count

  def allies(self):
    player = self.player()
    known_heroes = [hero for hero in self.heroes if hero != 'unknown']
    if player is not None:
      return [hero for hero in known_heroes if hero != player]
    return known_heroes
