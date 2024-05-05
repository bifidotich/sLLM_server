cd /d %~dp0
call venv\Scripts\activate.bat 
python run_server.py
cmd.exe