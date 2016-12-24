from roles import Roles

class Team:
  def __init__(self, heroes):
    self.heroes = heroes
    self.positions = {}

  def add(self, hero, position):
    if hero == 'unknown' or hero not in self.heroes:
      self.heroes.append(hero)

    if hero not in self.positions or position < self.positions[hero]:
      self.positions[hero] = position

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
    return len([hero for hero in self.heroes if hero != 'unknown'])

  # Returns true if the whole team was detected, even if that includes some
  # unselected slots.
  def fully_detected(self):
    return len(self.heroes) == 6

  def empty(self):
    return self.size() < 1

  def full(self):
    return self.size() == 6

  def __str__(self):
    return ", ".join(self.heroes)
