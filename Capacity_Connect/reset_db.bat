@echo off
title Reset Capacity Connect Demo Data
cd /d "%~dp0"
echo Resetting and reseeding database...
python seed_data.py
echo Database reset complete!
pause
