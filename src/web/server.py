import cv2
import os

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

from src.models.hero_picker import HeroPicker
from src.models.team import Team
from src.models.team_detector import TeamDetector

UPLOAD_FOLDER = 'src/web/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_teams(screenshot_path):
  team_detector = TeamDetector(cv2.imread(screenshot_path))
  team_detector.detect()
  return (team_detector.blue_team, team_detector.red_team)

def save_upload(file):
  timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
  filename = secure_filename(timestamp + '-' + file.filename)
  path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  file.save(path)
  return path

def render_result(red_team, blue_team):
  hero_picker = HeroPicker(red_team, blue_team)
  picks = hero_picker.pick()

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
    any_enemies=len(enemies) > 0, hero_names=Team.hero_names, player=player, \
    player_ok=player_ok, any_picks=any_picks)

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
    (blue_team, red_team) = get_teams(screenshot_path)
    template = render_result(red_team, blue_team)
    os.remove(screenshot_path)
    return template

  return redirect(request.url)
