from roles import Roles

class Team:
  def __init__(self, heroes):
    self.heroes = set(heroes)

  def add(self, hero):
    self.heroes.add(hero)

  def num_in_role(self, pool):
    count = 0
    for hero in pool:
      if hero in self.heroes:
        count += 1
    return count

  def num_healers(self):
    return self.num_in_role(Roles.healers)

  def num_support(self):
    return self.num_in_role(Roles.support)

  def num_offense(self):
    return self.num_in_role(Roles.offense)

  def num_tanks(self):
    return self.num_in_role(Roles.tanks)

  def any_offense(self):
    return self.num_offense() > 0

  def any_healers(self):
    return self.num_healers() > 0

  def any_tanks(self):
    return self.num_tanks() > 0

  def size(self):
    return len(self.heroes)

  def empty(self):
    return self.size() < 1

  def __str__(self):
    return ", ".join(self.heroes)
