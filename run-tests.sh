#!/bin/sh
coverage run --branch --source=src -m unittest test.hero_picker_test \
  test.team_test test.blue_team_test test.red_team_test && coverage report -m
