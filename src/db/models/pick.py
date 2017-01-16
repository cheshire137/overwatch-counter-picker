from datetime import datetime
from sqlalchemy import Date, cast

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

  def heroes_str(self):
    return ','.join(self.heroes())

  def blue_heroes_str(self):
    return ','.join(self.blue_heroes())

  def red_heroes_str(self):
    return ','.join(self.red_heroes())

  # Returns a list of the other players on the blue team, excluding the player
  # if the player is known.
  def allies(self):
    if self.player is None:
      return self.blue_heroes()
    result = []
    hero_counts = self.blue_team.counts()
    for hero, count in hero_counts.iteritems():
      if (hero != self.player and count > 0) or (hero == self.player and count > 1):
        result.append(hero)
    return result

  # Returns a string to be used to uniquely represent this Pick in a URL.
  def slug(self):
    date = self.uploaded_at.strftime('%Y%m%d')
    if self.player:
      return self.player + '.' + str(self.id) + '.' + date
    else:
      return 'unknown.' + str(self.id) + '.' + date

  # Given a slug like ana.1.20170115, this will return the Pick record that matches,
  # or None if it does not exist.
  @classmethod
  def find_by_slug(cls, slug):
    parts = slug.split('.')
    if len(parts) != 3:
      return None
    player = parts[0]
    id = int(parts[1])
    date_str = parts[2]
    row = Pick.query.filter_by(id=id).limit(1).first()
    if row and (row.player == player or row.player is None and player == 'unknown'):
      expected_date_str = row.uploaded_at.strftime('%Y%m%d')
      if date_str == expected_date_str:
        return row
    return None

  @classmethod
  def find_today_with_attrs(cls, attrs):
    valid_names = Team.hero_names.keys()
    for hero in valid_names:
      if hero not in attrs:
        attrs[hero] = False
    today = datetime.utcnow().date()
    row = Pick.query.filter_by(**attrs).\
      filter(cast(Pick.uploaded_at, Date) == today).limit(1).first()
    if row:
      return row
    return None

  # Returns True if the hero the user was playing is a suggested pick for the
  # known team composition.
  def player_ok(self):
    if self.player is None:
      return True
    return self.player in self.heroes()
