import os
import cv2
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
from team import Team
from team_detector import TeamDetector
from hero_picker import HeroPicker

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

@app.route('/', methods=['POST'])
def upload():
  if 'file' not in request.files:
    return redirect(request.url)

  file = request.files['file']
  if file and file.filename != '' and allowed_file(file.filename):
    the_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = secure_filename(the_time + '-' + file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    screenshot = cv2.imread(path)
    team_detector = TeamDetector(screenshot)
    team_detector.detect()
    hero_picker = HeroPicker(team_detector.red_team, team_detector.blue_team)
    picks = hero_picker.pick()
    allies = team_detector.blue_team.allies()
    any_allies = len(allies) > 0
    enemies = team_detector.red_team.heroes
    any_enemies = len(enemies) > 0
    player = team_detector.blue_team.player()
    player_ok = False

    if player is not None:
      player_ok = player in picks
      picks.remove(player)

    os.remove(path)

    return render_template('result.html', picks=picks, num_picks=len(picks), \
                           allies=allies, enemies=enemies, \
                           any_allies=any_allies, any_enemies=any_enemies, \
                           hero_names=Team.hero_names, player=player,
                           player_ok=player_ok)

  return redirect(request.url)

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  site_env = os.getenv('SITE_ENV', 'development')
  if site_env == 'production':
    app.run(host='0.0.0.0', debug=False, use_reloader=False, port=port)
  else:
    app.run(debug=True, use_reloader=True, port=port)
