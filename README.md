
# Play Super Mario (web game) with your voice

By playing with the volume of the current microphone registered audio/noise you can command Super Mario.

Funny video of my housemate playing (click for the video):
[![youtube video](video_youtube.gif)](https://youtu.be/7neh0ieFx0E)

# Install
You'll need:
* [PyQt4](https://pypi.python.org/pypi/PyQt4) `sudo apt-get install python-qt4`
* [pyqtgraph](http://www.pyqtgraph.org/) `sudo pip install pyqtgraph`
* [numpy](http://www.numpy.org/) `sudo apt-get install python-numpy`
* [pykeyboard](https://github.com/SavinaRoja/PyUserInput/tree/master/pykeyboard) `sudo pip install PyUserInput`
* [pyaudio](https://people.csail.mit.edu/hubert/pyaudio/) `sudo pip install pyaudio`. **Note**: You may get rid of this dependence modifying the code using the hacky approach found in [this gist](https://gist.github.com/awesomebytes/a382d94c0b312d9b507051b99a433a31). Do it at your own risk.

# Run

    python play_mario.py

And now when the sound registered by your microphone is louder than 12.5% **D** key will be pressed (so Mario will start moving right) when the noise becomes lower the key will be released. When the audio is louder than 25.0% **W** will be pressed (Mario will jump as high as relative to the maximum volume found at that moment). So if you make a louder noise it will jump higher!

You can adjust these parameters as you wish in the code.

# Thanks to
Based on  [qt audio monitor](https://github.com/swharden/Python-GUI-examples).

PROJECT PAGE: http://www.swharden.com/wp/2016-07-31-real-time-audio-monitor-with-pyqt/

![demo](demo.gif)
