from src.db.models.shared import db
from src.models.team import Team

class TeamComposition(db.Model):
  __tablename__ = 'team_compositions'

  id = db.Column(db.Integer, primary_key=True)

  ana = db.Column(db.Integer, default=0, nullable=False)
  bastion = db.Column(db.Integer, default=0, nullable=False)
  dva = db.Column(db.Integer, default=0, nullable=False)
  genji = db.Column(db.Integer, default=0, nullable=False)
  hanzo = db.Column(db.Integer, default=0, nullable=False)
  junkrat = db.Column(db.Integer, default=0, nullable=False)
  lucio = db.Column(db.Integer, default=0, nullable=False)
  mccree = db.Column(db.Integer, default=0, nullable=False)
  mei = db.Column(db.Integer, default=0, nullable=False)
  mercy = db.Column(db.Integer, default=0, nullable=False)
  pharah = db.Column(db.Integer, default=0, nullable=False)
  reaper = db.Column(db.Integer, default=0, nullable=False)
  reinhardt = db.Column(db.Integer, default=0, nullable=False)
  roadhog = db.Column(db.Integer, default=0, nullable=False)
  soldier76 = db.Column(db.Integer, default=0, nullable=False)
  sombra = db.Column(db.Integer, default=0, nullable=False)
  symmetra = db.Column(db.Integer, default=0, nullable=False)
  torbjorn = db.Column(db.Integer, default=0, nullable=False)
  tracer = db.Column(db.Integer, default=0, nullable=False)
  widowmaker = db.Column(db.Integer, default=0, nullable=False)
  winston = db.Column(db.Integer, default=0, nullable=False)
  zarya = db.Column(db.Integer, default=0, nullable=False)
  zenyatta = db.Column(db.Integer, default=0, nullable=False)

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs)

  # Returns an existing TeamComposition record for the given dictionary of hero
  # counts, or None if it does not exist in the database.
  @classmethod
  def find_with_counts(cls, counts):
    counts.pop('unknown', None)
    valid_names = Team.hero_names.keys()
    for hero in valid_names:
      if hero not in counts:
        counts[hero] = 0
    row = TeamComposition.query.filter_by(**counts).limit(1).first()
    if row:
      return row
    return None

  # Returns a dictionary for the given heroes list representing how many times
  # each hero appears in the list.
  @classmethod
  def counts_from_list(cls, heroes):
    counts = {}
    for hero in heroes:
      if hero not in counts:
        counts[hero] = 0
      counts[hero] = counts[hero] + 1
    return counts

  # Returns a dictionary of the heroes in this team composition and the number
  # of each.
  def counts(self):
    valid_names = Team.hero_names.keys()
    result = {}
    for hero in valid_names:
      if hero in self.__dict__:
        result[hero] = self.__dict__[hero]
    return result

  # Returns a list of the names of the heroes picked on this team.
  def heroes(self):
    valid_names = Team.hero_names.keys()
    picked_heroes = [name for name in valid_names if name in self.__dict__ and self.__dict__[name] > 0]
    picked_heroes.sort()
    return picked_heroes
