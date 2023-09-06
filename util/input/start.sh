#!/bin/sh
Xvfb :99 &    # Start xvfb on display 99 in the background
export DISPLAY=:99
flask run --port=5000 --host=0.0.0.0 --reload
