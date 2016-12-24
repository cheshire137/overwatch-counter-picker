import os
import cv2
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
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
    return render_template('result.html', picks=picks, num_picks=len(picks), \
                           allies=allies, enemies=enemies, \
                           any_allies=any_allies, any_enemies=any_enemies)

  return redirect(request.url)

if __name__ == '__main__':
  app.run(debug=True, use_reloader=True)
