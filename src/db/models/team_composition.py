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

  def __init__(self, ana=None, bastion=None, dva=None, genji=None, hanzo=None, junkrat=None, lucio=None, mccree=None, mei=None, mercy=None, pharah=None, reaper=None, reinhardt=None, roadhog=None, soldier76=None, sombra=None, symmetra=None, torbjorn=None, tracer=None, widowmaker=None, winston=None, zarya=None, zenyatta=None):
    self.ana = ana
    self.bastion = bastion
    self.dva = dva
    self.genji = genji
    self.hanzo = hanzo
    self.junkrat = junkrat
    self.lucio = lucio
    self.mccree = mccree
    self.mei = mei
    self.mercy = mercy
    self.pharah = pharah
    self.reaper = reaper
    self.reinhardt = reinhardt
    self.roadhog = roadhog
    self.soldier76 = soldier76
    self.sombra = sombra
    self.symmetra = symmetra
    self.torbjorn = torbjorn
    self.tracer = tracer
    self.widowmaker = widowmaker
    self.winston = winston
    self.zarya = zarya
    self.zenyatta = zenyatta

  # Returns a new instance of TeamComposition initialized with the given list of heroes.
  @classmethod
  def from_list(cls, heroes):
    counts = {}
    for hero in heroes:
      if hero not in counts:
        counts[hero] = 0
      counts[hero] = counts[hero] + 1
    return TeamComposition(**counts)
