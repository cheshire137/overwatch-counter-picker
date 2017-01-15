from datetime import datetime

from src.db.models.shared import db

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

  def __init__(self, screenshot_width=None, screenshot_height=None, \
               blue_team_id=None, red_team_id=None, player=None, ana=None, \
               bastion=None, dva=None, genji=None, hanzo=None, junkrat=None, \
               lucio=None, mccree=None, mei=None, mercy=None, pharah=None, \
               reaper=None, reinhardt=None, roadhog=None, soldier76=None, \
               sombra=None, symmetra=None, torbjorn=None, tracer=None, \
               widowmaker=None, winston=None, zarya=None, zenyatta=None):
    self.screenshot_width = screenshot_width
    self.screenshot_height = screenshot_height
    self.blue_team_id = blue_team_id
    self.red_team_id = red_team_id
    self.player = player
    self.uploaded_at = datetime.utcnow()

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
