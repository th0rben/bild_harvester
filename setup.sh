#!/bin/bash
sudo timedatectl set-timezone Europe/Berlin #change to your timezone
sudo apt-get install python3
sudo apt-get install python3-pip
sudo apt-get install python3-bs4
cd cron
sudo chmod +x cron_pull.sh
sudo crontab cronjob.txt