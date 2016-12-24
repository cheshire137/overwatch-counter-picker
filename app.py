import cv2
import sys

from team_detector import TeamDetector
from hero_picker import HeroPicker

# file_name = 'full-teams.jpg'
# if len(sys.argv) > 1:
#   file_name = sys.argv[1]
#   print 'Using screenshot', file_name, '\n'
# else:
#   print 'You can pass a file name from sample-screenshots/'
#   print 'Example: python', sys.argv[0], 'sample_screenshot.jpg\n'
#   print 'Using default screenshot', file_name, '\n'

# path = 'sample-screenshots/' + file_name
# screenshot = cv2.imread(path)
# team_detector = TeamDetector(screenshot)
# team_detector.detect()

# print 'Red team:', team_detector.red_team
# print 'Blue team:', team_detector.blue_team

# output_path = 'res.png'
# cv2.imwrite(output_path, screenshot)
# print '\nLook at', output_path, 'to see Overwatch hero detection'

fake_red_team = ['mercy', 'lucio', 'dva', 'genji', 'tracer', 'reinhardt']
fake_blue_team = ['dva', 'genji', 'hanzo', 'widowmaker', 'mccree']

print 'if red team is', fake_red_team
print 'and blue team is', fake_blue_team
hero_picker = HeroPicker(fake_red_team, fake_blue_team)
heroes = hero_picker.pick()
if len(heroes) == 1:
  print 'play', heroes[0]
else:
  print 'play one of', heroes

fake_red_team = ['hanzo', 'lucio', 'reaper', 'genji', 'tracer', 'reinhardt']
fake_blue_team = ['mercy', 'genji', 'hanzo', 'widowmaker', 'mccree']

print '\nif red team is', fake_red_team
print 'and blue team is', fake_blue_team
hero_picker = HeroPicker(fake_red_team, fake_blue_team)
heroes = hero_picker.pick()
if len(heroes) == 1:
  print 'play', heroes[0]
else:
  print 'play one of', heroes

fake_red_team = ['hanzo', 'lucio', 'reaper', 'genji', 'mei', 'reinhardt']
fake_blue_team = ['mercy', 'reinhardt', 'hanzo', 'widowmaker', 'bastion']

print '\nif red team is', fake_red_team
print 'and blue team is', fake_blue_team
hero_picker = HeroPicker(fake_red_team, fake_blue_team)
heroes = hero_picker.pick()
if len(heroes) == 1:
  print 'play', heroes[0]
else:
  print 'play one of', heroes
