#!/bin/bash
cd /git/news-scraper
git pull
echo "Last pull: $(date)" >> cron.log