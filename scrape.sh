sudo apt-get update
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
sudo apt install -y firefox-esr
python main.py
