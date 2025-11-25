@echo off
REM Run Django development server for tantawy project
cd /d %~dp0
python manage.py runserver 0.0.0.0:8000