# Raspberry Code
This part of the code is dedicated to the Raspberry PI.  
This includes managing the connection to the App, displaying content on the display and some game logic.  


You need to run the `main.py` with `python3` from the root directory of this repository. Just like this:  
`sudo python3 /home/pi/PingPongLedWall/Raspberry_Code/main.py`  

Don't forget to install the necessary pip packages:
- board
- rpi_ws281x
- adafruit-circuitpython-neopixel
- sudo python3 -m pip install --force-reinstall adafruit-blinka
- opensimplex
- matplotlib
- scikit-image
- configparser
- tuyalinksdk

Or simply use these commands:  
`sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel opensimplex matplotlib scikit-image configparser tuyalinksdk`  
`sudo python3 -m pip install --force-reinstall adafruit-blinka`  
