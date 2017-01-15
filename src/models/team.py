from src.models.roles import Roles

class Team:
  hero_names = {
    'ana': 'Ana',
    'bastion': 'Bastion',
    'dva': 'D.Va',
    'genji': 'Genji',
    'hanzo': 'Hanzo',
    'junkrat': 'Junkrat',
    'lucio': 'Lucio',
    'mccree': 'McCree',
    'mei': 'Mei',
    'mercy': 'Mercy',
    'pharah': 'Pharah',
    'reaper': 'Reaper',
    'reinhardt': 'Reinhardt',
    'roadhog': 'Roadhog',
    'soldier76': 'Soldier 76',
    'sombra': 'Sombra',
    'symmetra': 'Symmetra',
    'torbjorn': 'Torbjorn',
    'tracer': 'Tracer',
    'widowmaker': 'Widowmaker',
    'winston': 'Winston',
    'zarya': 'Zarya',
    'zenyatta': 'Zenyatta'
  }

  def __init__(self, heroes):
    self.heroes = heroes
    self.positions = dict([i, self.heroes[i]] for i in range(0, len(self.heroes)))

  def add(self, hero, position):
    if hero == 'unknown' or hero not in self.heroes:
      self.positions[position] = hero

    # Sort heroes left to right
    left_to_right = sorted(self.positions)
    self.heroes = [self.positions[position] for position in left_to_right]

  def num_in_role(self, pool):
    count = 0
    valid_heroes = [hero for hero in self.heroes if hero != 'unknown']
    for hero in pool:
      if hero in valid_heroes:
        count += 1
    return count

  def num_healers(self):
    return self.num_in_role(Roles.healers)

  def num_defense(self):
    return self.num_in_role(Roles.defense)

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

  # Returns the size of the team based on selected heroes.
  def size(self):
    return len([hero for hero in self.heroes if hero != 'unknown'])

  # Returns true if the whole team was detected, even if that includes some
  # unselected slots.
  def fully_detected(self):
    return len(self.heroes) == 6

  # Returns true if no one has picked a hero yet.
  def empty(self):
    return self.size() < 1

  def __str__(self):
    return ", ".join(self.heroes)
