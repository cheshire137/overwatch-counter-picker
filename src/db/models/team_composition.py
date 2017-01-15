from src.db.models.shared import db

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

  # Returns a new instance of TeamComposition initialized with the given list of heroes.
  @classmethod
  def from_list(cls, heroes):
    counts = {}
    for hero in heroes:
      if hero not in counts:
        counts[hero] = 0
      counts[hero] = counts[hero] + 1
    return TeamComposition(**counts)
