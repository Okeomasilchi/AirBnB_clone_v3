#!/usr/bin/bash
# compress the current folder
tar -czvf Airbnb_v3.tar.gz --exclude=.git --exclude=__pycache__ --exclude=.venv .
