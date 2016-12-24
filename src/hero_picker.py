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

  healers = ['mercy', 'zenyatta', 'lucio', 'ana']

  tanks = ['reinhardt', 'dva', 'zarya', 'winston', 'roadhog']

  dps = ['genji', 'mccree', 'pharah', 'reaper', 'soldier-76', 'sombra', 'tracer']

  def __init__(self, red_team, blue_team):
    self.red_team = red_team
    self.blue_team = blue_team

  def any_in_role(self, pool):
    for hero in pool:
      if hero in self.blue_team:
        return True
    return False

  def any_dps(self):
    return self.any_in_role(self.__class__.dps)

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
    max_score = max(hero_points.values())
    return [k for k,v in hero_points.iteritems() if v == max_score]

  def best_dps(self):
    return self.best_in_role(self.__class__.dps)

  def best_healers(self):
    return self.best_in_role(self.__class__.healers)

  def best_tanks(self):
    return self.best_in_role(self.__class__.tanks)

  def pick(self):
    blue_slots_filled = len(self.blue_team)
    if blue_slots_filled == 5:
      if not self.any_healers():
        return self.best_healers()
      if not self.any_tanks():
        return self.best_tanks()
      if not self.any_dps():
        return self.best_dps()
