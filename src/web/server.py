import cv2
import os
import math

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import subqueryload

from src.models.hero_picker import HeroPicker
from src.models.team import Team
from src.models.team_detector import TeamDetector

from src.db.models.shared import db
from src.db.models.pick import Pick
from src.db.models.team_composition import TeamComposition

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
STATS_PER_PAGE = 10

app = Flask(__name__)
dev_db_url = 'postgresql://localhost/overwatch_counter_picker'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', dev_db_url)
app.config['UPLOAD_FOLDER'] = os.path.abspath('src/web/uploads')

db.app = app
db.init_app(app)

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
def render_result(picks, pick_record, team_detector):
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
    player=player, player_ok=player_ok, any_picks=any_picks, \
    pick=pick_record)

# Saves records to the database about the heroes that were detected and the
# hero suggestion(s) for the user to play.
def save_picks_to_database(picks, team_detector):
  blue_counts = TeamComposition.counts_from_list(team_detector.blue_team.heroes)
  blue_team_record = TeamComposition.find_for_list(**blue_counts)
  if blue_team_record is None:
    blue_team_record = TeamComposition(**blue_counts)
    db.session.add(blue_team_record)

  red_counts = TeamComposition.counts_from_list(team_detector.red_team.heroes)
  red_team_record = TeamComposition.find_for_list(**red_counts)
  if red_team_record is None:
    red_team_record = TeamComposition(**red_counts)
    db.session.add(red_team_record)

  db.session.flush()

  pick_attrs = {
    'screenshot_width': team_detector.hero_detector.original_w,
    'screenshot_height': team_detector.hero_detector.original_h,
    'player': team_detector.blue_team.player(),
    'blue_team_id': blue_team_record.id,
    'red_team_id': red_team_record.id
  }
  pick_attrs.update({hero: True for hero in picks})
  pick_record = Pick(**pick_attrs)
  db.session.add(pick_record)

  db.session.commit()

  return pick_record

# Returns a rendered page template showing the results of the hero selection,
# based on the given Overwatch screenshot file path.
def get_picks_from_screenshot(screenshot_path):
  team_detector = get_team_detector(screenshot_path)
  hero_picker = HeroPicker(team_detector.red_team, team_detector.blue_team)
  picks = hero_picker.pick()
  pick_record = save_picks_to_database(picks, team_detector)
  return render_result(picks, pick_record, team_detector)

# Returns a list of Pick instances from the database, ordered most recent first.
# Paginated based on the given page and STATS_PER_PAGE.
def get_pick_records(page=1):
  offset = (page - 1) * STATS_PER_PAGE
  return Pick.query.options(subqueryload(Pick.blue_team), \
                            subqueryload(Pick.red_team)).\
              order_by(Pick.uploaded_at.desc()).\
              limit(STATS_PER_PAGE).offset(offset).all()

# Returns how many pages there are of pick records, based on STATS_PER_PAGE
# records shown per page.
def get_pick_page_count():
  total_rows = Pick.query.count()
  return int(math.ceil(total_rows / float(STATS_PER_PAGE)))


###########################################################################
# Routes ##################################################################
###########################################################################

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/stats', methods=['GET'])
def stats():
  return render_template('stats.html', picks=get_pick_records(), \
                         num_pages=get_pick_page_count(), page=1)

@app.route('/stats/page/<page>', methods=['GET'])
def stats_page(page):
  page = int(page)
  return render_template('stats.html', picks=get_pick_records(page=page), \
                         num_pages=get_pick_page_count(), page=page)

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
