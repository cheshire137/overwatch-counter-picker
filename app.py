import cv2
import sys

from team_detector import TeamDetector

original_name = 'full-teams.jpg'
if len(sys.argv) > 1:
  original_name = sys.argv[1]
  print 'Using screenshot', original_name, '\n'
else:
  print 'You can pass a file name from sample-screenshots/'
  print 'Example: python', sys.argv[0], 'sample_screenshot.jpg\n'
  print 'Using default screenshot', original_name, '\n'

thickness = 2
blue = (255, 0, 0)
red = (0, 0, 255)

screenshot = cv2.imread('sample-screenshots/' + original_name)
team_detector = TeamDetector(screenshot)
team_detector.detect()

print 'Red team:', team_detector.red_team
print 'Blue team:', team_detector.blue_team

output_path = 'res.png'
cv2.imwrite(output_path, screenshot)
print '\nLook at', output_path, 'to see Overwatch hero detection'
