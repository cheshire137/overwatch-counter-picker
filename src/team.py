from roles import Roles

class Team:
  def __init__(self, heroes):
    self.heroes = heroes

  def any_in_role(self, pool):
    for hero in pool:
      if hero in self.heroes:
        return True
    return False

  def any_offense(self):
    return self.any_in_role(Roles.offense)

  def any_healers(self):
    return self.any_in_role(Roles.healers)

  def any_tanks(self):
    return self.any_in_role(Roles.tanks)

  def size(self):
    return len(self.heroes)
