import operator

from src.models.roles import Roles

class HeroPicker:
  # If there's an X, go one of Y
  counters = {
    'ana': ['genji', 'reaper', 'tracer'],
    'bastion': ['genji', 'tracer', 'widowmaker'],
    'dva': ['mei', 'symmetra', 'zenyatta'],
    'genji': ['mei', 'zarya', 'winston'],
    'hanzo': ['dva', 'tracer', 'widowmaker'],
    'junkrat': ['mccree', 'pharah', 'widowmaker'],
    'lucio': ['mei', 'mccree', 'pharah'],
    'mccree': ['genji', 'soldier76', 'widowmaker'],
    'mei': ['junkrat', 'pharah', 'widowmaker'],
    'mercy': ['mccree', 'tracer', 'widowmaker'],
    'pharah': ['mccree', 'roadhog', 'soldier76'],
    'reaper': ['junkrat', 'mccree', 'pharah'],
    'reinhardt': ['reaper', 'roadhog', 'symmetra'],
    'roadhog': ['dva', 'genji', 'reaper'],
    'soldier76': ['genji', 'mei', 'tracer'],
    'sombra': ['symmetra', 'mei', 'winston'],
    'symmetra': ['junkrat', 'pharah', 'roadhog'],
    'torbjorn': ['junkrat', 'pharah', 'widowmaker'],
    'tracer': ['mccree', 'mei', 'soldier76'],
    'widowmaker': ['dva', 'genji', 'winston'],
    'winston': ['mccree', 'mei', 'reaper'],
    'zarya': ['pharah', 'roadhog', 'reaper'],
    'zenyatta': ['hanzo', 'tracer', 'widowmaker']
  }

  # If you have X on your team, one of Y would pair well
  synergies = {
    'ana': [],
    'bastion': ['reinhardt', 'mercy'],
    'dva': ['mercy', 'ana'],
    'genji': ['lucio'],
    'hanzo': [],
    'junkrat': [],
    'lucio': [],
    'mccree': ['lucio'],
    'mei': ['roadhog'],
    'mercy': ['zarya', 'pharah', 'dva'],
    'pharah': ['mercy'],
    'reaper': [],
    'reinhardt': [],
    'roadhog': ['mei'],
    'soldier76': ['mercy'],
    'sombra': [],
    'symmetra': ['torbjorn'],
    'torbjorn': ['symmetra'],
    'tracer': ['lucio'],
    'widowmaker': ['winston', 'mercy'],
    'winston': [],
    'zarya': [],
    'zenyatta': []
  }

  map_types = ['control', 'assault', 'escort', 'hybrid']

  def __init__(self, red_team, blue_team, map_type=None, attacking=None):
    self.red_team = red_team
    self.blue_team = blue_team
    self.map_type = map_type

    self.attacking = attacking
    if self.map_type == 'control':
      self.attacking = True

  # Returns true if we are defending this round. Always false on control
  # maps like Nepal.
  def defending(self):
    return self.attacking != None and not self.attacking

  # Pick the best hero for you to play, based on who is on your team and
  # who is on the red team, if any enemies are known.
  def pick(self):
    all_heroes = self.counters.keys()

    if self.blue_team.size() < 4 and self.red_team.empty():
      return all_heroes # just play anyone

    any_healers = self.blue_team.any_healers()
    any_tanks = self.blue_team.any_tanks()
    any_offense = self.blue_team.any_offense()

    if not any_healers and not any_tanks and not any_offense:
      return self.pick_from_pool(Roles.healers + Roles.tanks + Roles.offense)
    elif not any_healers and not any_tanks:
      return self.pick_from_pool(Roles.healers + Roles.tanks)
    elif not any_healers and not any_offense:
      return self.pick_from_pool(Roles.healers + Roles.offense)
    elif not any_tanks and not any_offense:
      return self.pick_from_pool(Roles.tanks + Roles.offense)
    elif not any_healers:
      return self.best_healers()
    elif not any_tanks:
      return self.best_tanks()
    elif not any_offense:
      return self.best_offense()

    if not self.defending():
      # Try to have two healers.
      if self.blue_team.num_healers() < 2:
        return self.best_healers()

    # Try to have at least two tanks.
    if self.blue_team.num_tanks() < 2:
      return self.best_tanks()

    return self.pick_from_pool(all_heroes)

  # Pick the best offense hero to play.
  def best_offense(self):
    return self.pick_from_pool(Roles.offense)

  # Pick the best healer to play.
  def best_healers(self):
    return self.pick_from_pool(Roles.healers)

  # Pick the best tank to play.
  def best_tanks(self):
    return self.pick_from_pool(Roles.tanks)

  # Given a list of heroes to choose from, pick the best one(s) for you to
  # play, based on who is on your team and who is on the red team, if any
  # enemies are known.
  def pick_from_pool(self, pool):
    hero_points = {}
    num_support = self.blue_team.num_support()
    num_offense = self.blue_team.num_offense()
    num_defense = self.blue_team.num_defense()
    allies = self.blue_team.allies()

    for hero in pool:
      hero_points[hero] = 0

      # Avoid heroes that will be countered by the enemy team.
      counters = self.__class__.counters[hero]
      for enemy in self.red_team.heroes:
        if enemy in counters:
          hero_points[hero] -= 1

      # Which heroes work well with others on our team?
      synergies = self.__class__.synergies[hero]
      for ally in self.blue_team.allies():
        if ally in synergies:
          hero_points[hero] += 1

      # Defense heroes are good when we're defending.
      if self.defending():
        if hero in Roles.defense:
          hero_points[hero] += 1

      # Discourage more than 2 support heroes.
      if hero in Roles.support and num_support >= 2:
        hero_points[hero] -= 1

      # Discourage more than 3 offense heroes.
      if hero in Roles.offense and num_offense >= 3:
        hero_points[hero] -= 1

      # Heavily discourage duplicates.
      if hero in allies:
        hero_points[hero] -= 3

      # Discourage more than 3 offense + defense heroes.
      if (hero in Roles.offense or hero in Roles.defense) and num_offense + num_defense >= 3:
        hero_points[hero] -= 1

    sorted_hero_points = sorted(hero_points.items(), key=operator.itemgetter(1))
    best_score = max(dict(sorted_hero_points).values())
    return [hero for hero, score in sorted_hero_points if score == best_score]
