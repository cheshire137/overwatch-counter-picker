import os
import cv2

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime

from src.team import Team
from src.team_detector import TeamDetector
from src.hero_picker import HeroPicker

UPLOAD_FOLDER = 'src/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

def get_teams(screenshot_path):
  team_detector = TeamDetector(cv2.imread(path))
  team_detector.detect()
  return (team_detector.blue_team, team_detector.red_team)

def save_upload(file):
  timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
  filename = secure_filename(timestamp + '-' + file.filename)
  path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
  file.save(path)
  return path

def render_result(red_team, blue_team):
  hero_picker = HeroPicker(red_team, blue_team)
  picks = hero_picker.pick()
  player = blue_team.player()
  player_ok = False
  if player is not None:
    player_ok = player in picks
    if player_ok:
      picks.remove(player)
  any_picks = len(picks) > 0

  return render_template('result.html', picks=picks, num_picks=len(picks), \
    allies=blue_team.allies(), enemies=red_team.heroes, \
    any_allies=len(allies) > 0, any_enemies=len(enemies) > 0, \
    hero_names=Team.hero_names, player=player, player_ok=player_ok, \
    any_picks=any_picks)

@app.route('/', methods=['POST'])
def upload():
  if 'file' not in request.files:
    return redirect(request.url)

  file = request.files['file']
  if file and file.filename != '' and allowed_file(file.filename):
    path = save_upload(file)
    (blue_team, red_team) = get_teams(path)
    template = render_result(red_team, blue_team)
    os.remove(path)
    return template

  return redirect(request.url)

def run_app():
  port = int(os.environ.get('PORT', 5000))
  site_env = os.getenv('SITE_ENV', 'development')
  if site_env == 'production':
    app.run(host='0.0.0.0', debug=False, use_reloader=False, port=port)
  else:
    app.run(debug=True, use_reloader=True, port=port)

if __name__ == '__main__':
  run_app()
