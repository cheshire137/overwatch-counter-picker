from datetime import datetime

from src.db.models.shared import db
from src.db.models.team_composition import TeamComposition
from src.models.team import Team

class Pick(db.Model):
  __tablename__ = 'picks'

  id = db.Column(db.Integer, primary_key=True)

  screenshot_width = db.Column(db.Integer)
  screenshot_height = db.Column(db.Integer)

  blue_team_id = db.Column(db.Integer, db.ForeignKey('team_compositions.id'), index=True)
  red_team_id = db.Column(db.Integer, db.ForeignKey('team_compositions.id'), index=True)

  player = db.Column(db.String(10))

  ana = db.Column(db.Boolean, default=False, nullable=False)
  bastion = db.Column(db.Boolean, default=False, nullable=False)
  dva = db.Column(db.Boolean, default=False, nullable=False)
  genji = db.Column(db.Boolean, default=False, nullable=False)
  hanzo = db.Column(db.Boolean, default=False, nullable=False)
  junkrat = db.Column(db.Boolean, default=False, nullable=False)
  lucio = db.Column(db.Boolean, default=False, nullable=False)
  mccree = db.Column(db.Boolean, default=False, nullable=False)
  mei = db.Column(db.Boolean, default=False, nullable=False)
  mercy = db.Column(db.Boolean, default=False, nullable=False)
  pharah = db.Column(db.Boolean, default=False, nullable=False)
  reaper = db.Column(db.Boolean, default=False, nullable=False)
  reinhardt = db.Column(db.Boolean, default=False, nullable=False)
  roadhog = db.Column(db.Boolean, default=False, nullable=False)
  soldier76 = db.Column(db.Boolean, default=False, nullable=False)
  sombra = db.Column(db.Boolean, default=False, nullable=False)
  symmetra = db.Column(db.Boolean, default=False, nullable=False)
  torbjorn = db.Column(db.Boolean, default=False, nullable=False)
  tracer = db.Column(db.Boolean, default=False, nullable=False)
  widowmaker = db.Column(db.Boolean, default=False, nullable=False)
  winston = db.Column(db.Boolean, default=False, nullable=False)
  zarya = db.Column(db.Boolean, default=False, nullable=False)
  zenyatta = db.Column(db.Boolean, default=False, nullable=False)

  uploaded_at = db.Column(db.DateTime, nullable=False)

  blue_team = db.relationship('TeamComposition', foreign_keys=blue_team_id)
  red_team = db.relationship('TeamComposition', foreign_keys=red_team_id)

  def __init__(self, **kwargs):
    self.uploaded_at = datetime.utcnow()
    self.__dict__.update(kwargs)

  def blue_heroes(self):
    if self.blue_team:
      return self.blue_team.heroes()
    return []

  def red_heroes(self):
    if self.red_team:
      return self.red_team.heroes()
    return []

  # Returns the count of how many heroes were suggested to the user.
  def num_suggestions(self):
    valid_names = Team.hero_names.keys()
    suggestions = [name for name in valid_names if name in self.__dict__ and self.__dict__[name]]
    return len(suggestions)

  # Returns a list of the names of the heroes suggested for the user to pick.
  def heroes(self):
    valid_names = Team.hero_names.keys()
    suggestions = [name for name in valid_names if name in self.__dict__ and self.__dict__[name]]
    suggestions.sort()
    return suggestions

  # Returns True if the hero the user was playing is a suggested pick for the
  # known team composition.
  def player_ok(self):
    if self.player is None:
      return True
    return self.player in self.heroes()
