import cv2
import os

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

from src.models.hero_picker import HeroPicker
from src.models.team import Team
from src.models.team_detector import TeamDetector

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
dev_db_url = 'postgresql://localhost/overwatch_counter_picker'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', dev_db_url)
app.config['UPLOAD_FOLDER'] = os.path.abspath('src/web/uploads')

db = SQLAlchemy(app)


###########################################################################
# Database models #########################################################
###########################################################################

class Team(db.Model):
  __tablename__ = 'teams'

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

  def __init__(self, heroes=[]):
    for hero in heroes:
      self[hero] = self[hero] + 1

class Pick(db.Model):
  __tablename__ = 'picks'

  id = db.Column(db.Integer, primary_key=True)

  screenshot_width = db.Column(db.Integer)
  screenshot_height = db.Column(db.Integer)

  blue_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), index=True)
  red_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), index=True)

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

  blue_team = db.relationship('Team', foreign_keys=blue_team_id)
  red_team = db.relationship('Team', foreign_keys=red_team_id)

  def __init__(self, attrs={}):
    self.screenshot_width = attrs['width']
    self.screenshot_height = attrs['height']
    self.blue_team_id = attrs['blue_team_id']
    self.red_team_id = attrs['red_team_id']
    self.player = attrs['player']
    for pick in attrs['picks']:
      self[pick] = True
    self.uploaded_at = datetime.utcnow()


###########################################################################
# Utility functions #######################################################
###########################################################################

# Returns true if the given file name is an allowed file type.
def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Returns a TeamDetector instance, with heroes already detected, for the given
# screenshot.
def get_team_detector(screenshot_path):
  team_detector = TeamDetector(cv2.imread(screenshot_path))
  team_detector.detect()
  return team_detector

# Saves the given file to the upload folder and returns the path where it is
# saved.
def save_upload(file):
  timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
  filename = secure_filename(timestamp + '-' + file.filename)
  path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
  file.save(path)
  return path

# Render the result.html template with information about the heroes that were
# detected and the hero(es) the user should play in this team composition.
def render_result(picks, team_detector):
  blue_team = team_detector.blue_team
  red_team = team_detector.red_team

  allies = blue_team.allies()
  enemies = red_team.heroes

  player = blue_team.player()
  player_ok = False
  if player is not None:
    player_ok = player in picks
    if player_ok:
      picks.remove(player)
  any_picks = len(picks) > 0

  return render_template('result.html', picks=picks, num_picks=len(picks), \
    allies=allies, enemies=enemies, any_allies=len(allies) > 0, \
    any_enemies=not red_team.empty(), hero_names=Team.hero_names, \
    player=player, player_ok=player_ok, any_picks=any_picks)

# Saves a new record to the 'picks' table about the heroes that were detected
# and the hero suggestion(s) for the user to play.
def save_pick_record(picks, team_detector):
  blue_team_record = Team(team_detector.blue_team.heroes)
  db.session.add(blue_team_record)

  red_team_record = Team(team_detector.red_team.heroes)
  db.session.add(red_team_record)

  db.session.flush()

  pick_attrs = {
    'width': team_detector.hero_detector.original_w,
    'height': team_detector.hero_detector.original_h,
    'picks': picks,
    'player': team_detector.blue_team.player(),
    'blue_team_id': blue_team_record.id,
    'red_team_id': red_team_record.id
  }
  db.session.add(Pick(pick_attrs))

  db.session.commit()

# Returns a rendered page template showing the results of the hero selection,
# based on the given Overwatch screenshot file path.
def get_picks_from_screenshot(screenshot_path):
  team_detector = get_team_detector(screenshot_path)
  hero_picker = HeroPicker(team_detector.red_team, team_detector.blue_team)
  picks = hero_picker.pick()
  save_pick_record(picks, team_detector)
  return render_result(picks, team_detector)


###########################################################################
# Routes ##################################################################
###########################################################################

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/', methods=['POST'])
def upload():
  if 'file' not in request.files:
    return redirect(request.url)

  file = request.files['file']
  if file and file.filename != '' and allowed_file(file.filename):
    screenshot_path = save_upload(file)
    template = get_picks_from_screenshot(screenshot_path)
    os.remove(screenshot_path)
    return template

  return redirect(request.url)
