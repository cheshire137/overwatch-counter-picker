# Overwatch Counter Picker

[![Build status](https://travis-ci.org/cheshire137/overwatch-counter-picker.svg?branch=master)](https://travis-ci.org/cheshire137/overwatch-counter-picker)

This is a work in progress to tell you the best hero to pick in Overwatch to
counter the enemy team, based on a provided screenshot of your team composition.

## How to Run

You will need Python 2.7 and OpenCV installed. See detailed instructions below for
OpenCV installation on macOS.

```bash
pip install -r requirements.txt
```

### Server

The server will run at [127.0.0.1:5000](http://127.0.0.1:5000/) and let you
upload an Overwatch screenshot for determining which hero to pick. Run with
`python src/server.py`.

### Command-Line Script

The command-line script will allow you to pass an Overwatch screenshot and
determine which hero you should pick. Run with `python src/cli.py`. You can pass
it the name of an image in the sample-screenshots/ folder, e.g.,
`python src/cli.py hero-selection-not-full.jpg`.

### How to Install OpenCV

Here's how I did it in macOS Sierra using Homebrew. Basically follow
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

`python -m unittest test.hero_picker_test`

## How to Deploy to Heroku

```bash
heroku login
heroku create your_app_name
heroku buildpacks:set https://github.com/slobdell/heroku-buildpack-python-opencv-scipy
git push heroku master
```
