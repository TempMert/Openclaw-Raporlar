#!/bin/bash
# Daily report pipeline: fetch tweets -> generate HTML -> push
cd /home/openclaw/.openclaw/workspace
python3 fetch_tweets.py
python3 generate_report.py
