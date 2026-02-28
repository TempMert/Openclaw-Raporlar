#!/bin/bash
# Daily report pipeline: fetch tweets -> generate HTML -> validate -> push
cd /home/openclaw/.openclaw/workspace
python3 fetch_tweets.py
python3 generate_report.py
echo "Running validation tests..."
python3 test_report.py >> report_test.log 2>&1
if [ $? -ne 0 ]; then
  echo "❌ Report validation FAILED - check report_test.log"
else
  echo "✅ Report validation PASSED"
fi
