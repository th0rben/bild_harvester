#!/bin/bash
pip install beautifulsoup4
cd cron
sudo chmod +x cron_pull.sh
sudo crontab cronjob.txt