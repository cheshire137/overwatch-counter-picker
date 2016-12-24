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
    'mccree': ['genji', 'soldier-76', 'widowmaker'],
    'mei': ['junkrat', 'pharah', 'widowmaker'],
    'mercy': ['mccree', 'tracer', 'widowmaker'],
    'pharah': ['mccree', 'roadhog', 'soldier-76'],
    'reaper': ['junkrat', 'mccree', 'pharah'],
    'reinhardt': ['reaper', 'roadhog', 'symmetra'],
    'roadhog': ['dva', 'genji', 'reaper'],
    'soldier-76': ['genji', 'mei', 'tracer'],
    'sombra': ['symmetra', 'mei', 'winston'],
    'symmetra': ['junkrat', 'pharah', 'roadhog'],
    'torbjorn': ['junkrat', 'pharah', 'widowmaker'],
    'tracer': ['mccree', 'mei', 'soldier-76'],
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
    'soldier-76': ['mercy'],
    'sombra': [],
    'symmetra': ['torbjorn'],
    'torbjorn': ['symmetra'],
    'tracer': ['lucio'],
    'widowmaker': ['winston', 'mercy'],
    'winston': [],
    'zarya': [],
    'zenyatta': []
  }

  healers = ['mercy', 'zenyatta', 'lucio', 'ana']

  tanks = ['reinhardt', 'dva', 'zarya', 'winston', 'roadhog']

  offense = ['genji', 'mccree', 'pharah', 'reaper', 'soldier-76', 'sombra',
             'tracer']

  map_types = ['control', 'assault', 'escort', 'hybrid']

  def __init__(self, red_team, blue_team, map_type=None, offense=None):
    self.red_team = red_team
    self.blue_team = blue_team
    self.map_type = map_type
    self.offense = offense

    if self.map_type == 'control'
      self.offense = True

  def any_in_role(self, pool):
    for hero in pool:
      if hero in self.blue_team:
        return True
    return False

  def any_offense(self):
    return self.any_in_role(self.__class__.offense)

  def any_healers(self):
    return self.any_in_role(self.__class__.healers)

  def any_tanks(self):
    return self.any_in_role(self.__class__.tanks)

  def best_in_role(self, pool):
    hero_points = {}
    for hero in pool:
      hero_points[hero] = 0

      counters = self.__class__.counters[hero]
      for enemy in self.red_team:
        if enemy in counters:
          hero_points[hero] -= 1

      synergies = self.__class__.synergies[hero]
      for ally in self.blue_team:
        if ally in synergies:
          hero_points[hero] += 1

    max_score = max(hero_points.values())
    return [k for k,v in hero_points.iteritems() if v == max_score]

  def best_offense(self):
    return self.best_in_role(self.__class__.offense)

  def best_healers(self):
    return self.best_in_role(self.__class__.healers)

  def best_tanks(self):
    return self.best_in_role(self.__class__.tanks)

  def pick(self):
    red_slots_filled = len(self.red_team)
    blue_slots_filled = len(self.blue_team)
    all_heroes = counters.keys()

    if blue_slots_filled < 4:
      return all_heroes # just play anyone

    if blue_slots_filled == 5:
      if not self.any_healers():
        return self.best_healers()
      if not self.any_tanks():
        return self.best_tanks()
      if not self.any_offense():
        return self.best_offense()
      if red_slots_filled > 0:
        return self.best_in_role(all_heroes)
