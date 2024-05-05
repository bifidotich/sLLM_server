cd /d %~dp0

call python -m venv venv
call venv\Scripts\activate.bat 
call python.exe -m pip install --upgrade pip
pip install -r requirements.txt
call pip3 install torch --index-url https://download.pytorch.org/whl/cu121

cmd.exe


