#!/bin/bash
cd /home/git/news-scraper #change to your directory
git pull
echo "Last pull: $(date)" >> cron.log
cd src
python3 main.py