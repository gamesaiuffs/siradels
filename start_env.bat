@echo off
set "DIR_ATUAL=%CD%"
cd /d venv\Scripts
call activate
cd /d "%DIR_ATUAL%"