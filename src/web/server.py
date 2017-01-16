import cv2
import os
import math

from datetime import datetime, date
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

# Saves records to the database about the heroes that were detected and the
# hero suggestion(s) for the user to play.
def save_picks_to_database(picks, team_detector):
  player = team_detector.blue_team.player()

  if not player:
    return None

  blue_counts = TeamComposition.counts_from_list(team_detector.blue_team.heroes)
  blue_team_record = TeamComposition.find_with_counts(blue_counts)
  if blue_team_record is None:
    blue_team_record = TeamComposition(**blue_counts)
    db.session.add(blue_team_record)

  red_counts = TeamComposition.counts_from_list(team_detector.red_team.heroes)
  red_team_record = TeamComposition.find_with_counts(red_counts)
  if red_team_record is None:
    red_team_record = TeamComposition(**red_counts)
    db.session.add(red_team_record)

  db.session.flush()

  pick_attrs = {
    'screenshot_width': team_detector.hero_detector.original_w,
    'screenshot_height': team_detector.hero_detector.original_h,
    'player': player,
    'blue_team_id': blue_team_record.id,
    'red_team_id': red_team_record.id
  }
  pick_attrs.update({hero: True for hero in picks})

  pick_record = Pick.find_today_with_attrs(pick_attrs)
  if pick_record is None:
    pick_record = Pick(**pick_attrs)
    db.session.add(pick_record)

  db.session.commit()

  return pick_record

# Returns a Pick database record for the results of the hero selection,
# based on the given Overwatch screenshot file path.
def get_pick_record_from_screenshot(screenshot_path):
  team_detector = get_team_detector(screenshot_path)
  hero_picker = HeroPicker(team_detector.red_team, team_detector.blue_team)
  picks = hero_picker.pick()
  return save_picks_to_database(picks, team_detector)

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

def static_file_hash(filename):
  return int(os.stat(filename).st_mtime)


###########################################################################
# App config ##############################################################
###########################################################################

@app.url_defaults
def hashed_url_for_static_file(endpoint, values):
  if 'static' == endpoint or endpoint.endswith('.static'):
    filename = values.get('filename')
    if filename:
      if '.' in endpoint: # has higher priority
        blueprint = endpoint.rsplit('.', 1)[0]
      else:
        blueprint = request.blueprint # can be None too

      if blueprint:
        static_folder = app.blueprints[blueprint].static_folder
      else:
        static_folder = app.static_folder

      param_name = 'h'
      while param_name in values:
        param_name = '_' + param_name
      values[param_name] = static_file_hash(os.path.join(static_folder, filename))

###########################################################################
# Routes ##################################################################
###########################################################################

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/pick/<slug>', methods=['GET'])
def pick(slug):
  pick_record = Pick.find_by_slug(slug)
  if pick_record is None:
    return render_template('404.html')
  player = pick_record.player
  picks = pick_record.heroes()
  player_ok = False
  if player is not None:
    player_ok = player in picks
    if player_ok:
      picks.remove(player)
  allies = pick_record.allies()
  enemies = pick_record.red_heroes()
  return render_template('pick.html', pick=pick_record, picks=picks, \
    num_picks=len(picks), allies=allies, enemies=enemies, \
    any_allies=len(allies) > 0, any_enemies=len(enemies) > 0, \
    hero_names=Team.hero_names, player=player, player_ok=player_ok, \
    any_picks=len(picks) > 0)

@app.route('/stats', methods=['GET'])
def stats():
  return render_template('stats.html', picks=get_pick_records(), \
                         num_pages=get_pick_page_count(), page=1)

@app.route('/bad-screenshot', methods=['GET'])
def bad_screenshot():
  return render_template('bad_screenshot.html')

@app.route('/stats/page/<page>', methods=['GET'])
def stats_page(page):
  try:
    page = int(page)
  except ValueError:
    return render_template('404.html')
  num_pages = get_pick_page_count()
  if page > num_pages or page < 1:
    return render_template('404.html')
  return render_template('stats.html', picks=get_pick_records(page=page), \
                         num_pages=num_pages, page=page)

@app.route('/', methods=['POST'])
def upload():
  if 'file' not in request.files:
    return redirect(request.url)

  file = request.files['file']
  if file and file.filename != '' and allowed_file(file.filename):
    screenshot_path = save_upload(file)
    pick_record = get_pick_record_from_screenshot(screenshot_path)
    os.remove(screenshot_path)
    if pick_record:
      return redirect('/pick/' + pick_record.slug())
    return redirect('/bad-screenshot')

  return redirect(request.url)
