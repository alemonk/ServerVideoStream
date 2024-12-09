# python -m venv .venv
source .venv/bin/activate

pip install websockets
pip install pillow
pip install RPi.GPIO
pip install opencv-python

sudo apt update
sudo apt install libcamera-apps
