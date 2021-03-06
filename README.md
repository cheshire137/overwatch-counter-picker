# Overwatch Counter Picker

[![Build status](https://travis-ci.org/cheshire137/overwatch-counter-picker.svg?branch=master)](https://travis-ci.org/cheshire137/overwatch-counter-picker)

This is a web app that tells you the best hero to pick in Overwatch to
counter the enemy team, based on a provided screenshot of your team composition.

![Screenshot of app](https://raw.githubusercontent.com/cheshire137/overwatch-counter-picker/master/app-screenshot.png)

## How to Run

You will need Python 2.7, pip, PostgreSQL, and OpenCV installed. See detailed
instructions below for OpenCV installation on macOS.

```bash
pip install -r requirements.txt # install required Python libraries
createdb overwatch_counter_picker # create the database
python -m src.db.create # create database tables
```

### Server

The server will run at [127.0.0.1:5000](http://127.0.0.1:5000/). Run with
`./server.sh`.

### Command-Line Script

The command-line script will allow you to pass an Overwatch screenshot and
determine which hero you should pick. It's useful because it produces an image
with boxes showing exactly which heroes were detected where. So if an upload to
the web app doesn't find all the players on a team, run the same image through
the command-line script for debugging what it "sees." Run with
`python -m src.cli`. You can pass it the path to an image, e.g.,
`python -m src.cli sample-screenshots/hero-selection-not-full.jpg`.

### How to Install OpenCV

Here's how I installed OpenCV in macOS Sierra using Homebrew. Basically follow
[this macOS OpenCV installation guide](http://www.pyimagesearch.com/2016/12/19/install-opencv-3-on-macos-with-homebrew-the-easy-way/),
namely:

```bash
brew install python python3
brew linkapps python
brew linkapps python3
brew tap homebrew/science
brew install opencv3 --with-contrib --with-python3 --HEAD
echo /usr/local/opt/opencv3/lib/python2.7/site-packages >> /usr/local/lib/python2.7/site-packages/opencv3.pth
mv /usr/local/opt/opencv3/lib/python3.5/site-packages/cv2.cpython-35m-darwin.so /usr/local/opt/opencv3/lib/python3.5/site-packages/cv2.so
echo /usr/local/opt/opencv3/lib/python3.5/site-packages >> /usr/local/lib/python3.5/site-packages/opencv3.pth
```

## How to Test

```bash
pip install -r requirements.txt
pip install coverage
./run-tests.sh
```

Tests will be run and a test coverage report will appear afterward.

You can run an individual test using its class and method name like so:

```bash
python -m test.hero_detector_test HeroDetectorTest.test_detect_finds_lucio_when_present
```

## How to Deploy to Heroku

```bash
heroku login
heroku create your_app_name
heroku buildpacks:set https://github.com/diogojc/heroku-buildpack-python-opencv-scipy
git push heroku master
heroku addons:create heroku-postgresql:hobby-dev # create database
heroku run python -m src.db.create # create tables
```

## Thanks

Thanks to Blizzard for Overwatch. The hero portraits and names are all theirs,
I'm just a fan. :heart:
