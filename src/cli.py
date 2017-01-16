import cv2
import sys
import os

from src.models.hero_picker import HeroPicker
from src.models.team_detector import TeamDetector

path = os.path.abspath('sample-screenshots/full-teams.jpg')
if len(sys.argv) > 1:
  path = sys.argv[1]
  print 'Using screenshot', path, '\n'
else:
  print 'You can pass a file name from sample-screenshots/'
  print 'Example: python', sys.argv[0], 'sample_screenshot.jpg\n'
  print 'Using default screenshot', path, '\n'

team_detector = TeamDetector(cv2.imread(path))
team_detector.detect(draw_boxes=True)
hero_detector = team_detector.hero_detector

if hero_detector.is_cards_screen:
  print 'Screenshot is of game-over screen with voting cards'

if hero_detector.resized_w != hero_detector.original_w:
  print 'Resized original image from', str(hero_detector.original_w) + 'x' + \
    str(hero_detector.original_h), 'to', str(hero_detector.resized_w) + 'x' + \
    str(hero_detector.resized_h), '\n'

print 'Red team:', team_detector.red_team
print 'Blue team:', team_detector.blue_team

player = team_detector.blue_team.player()
if player is None:
  print 'Player not detected!'
else:
  print 'Player is', player

output_path = 'res.png'
cv2.imwrite(output_path, team_detector.hero_detector.original)
print '\nLook at', output_path, 'to see Overwatch hero detection\n'

hero_picker = HeroPicker(team_detector.red_team, team_detector.blue_team)
picks = hero_picker.pick()
if len(picks) < 2:
  if player is not None and player == picks[0]:
    print 'Your choice of', player, 'is spot on!'
  else:
    print 'Play', picks[0]
else:
  print 'Play one of:', ', '.join(picks)
