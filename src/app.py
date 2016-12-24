import cv2
import sys
import os

from team_detector import TeamDetector
from hero_picker import HeroPicker

file_name = 'full-teams.jpg'
if len(sys.argv) > 1:
  file_name = sys.argv[1]
  print 'Using screenshot', file_name, '\n'
else:
  print 'You can pass a file name from sample-screenshots/'
  print 'Example: python', sys.argv[0], 'sample_screenshot.jpg\n'
  print 'Using default screenshot', file_name, '\n'

path = os.path.abspath('sample-screenshots/' + file_name)
screenshot = cv2.imread(path)
team_detector = TeamDetector(screenshot)
team_detector.detect()

print 'Red team:', team_detector.red_team
print 'Blue team:', team_detector.blue_team

output_path = 'res.png'
cv2.imwrite(output_path, screenshot)
print '\nLook at', output_path, 'to see Overwatch hero detection\n'

hero_picker = HeroPicker(team_detector.red_team, team_detector.blue_team)
picks = hero_picker.pick()
if len(picks) < 2:
  print 'Play', picks[0]
else:
  print 'Play one of', ', '.join(picks)
