#!/bin/bash

now=$(date +"%Y-%m-%d %H:%M:%S")
echo "===> Job starting time: $now"

. venv/bin/activate

python run/run_scraper.py
python run/insert_market_shot.py


now=$(date +"%Y-%m-%d %H:%M:%S")
echo "===> Job finising time: $now"
