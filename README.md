# network-pong
implementation of a 2 player pong game using OSC as the communication protocol

###Dependencies

- python 2.x

- pyprocessing library [LINK](https://code.google.com/p/pyprocessing/)

- pyliblo [LINK](http://das.nasophon.de/pyliblo/)

###Instructions

To install the dependencies using pip:

		cd network-pong

		sudo pip install -r requirements.txt

I you don't have pip installed, you can do it by following the instructions on this [LINK](https://pip.pypa.io/en/latest/installing.html)

You can also install them manually via the links posted before.

After installing the dependencies, download a copy of the repository in two different computers. To run the app cd to the folder and type: 

		python main.py

###API

Two files make the library for the pong game. pong-elements.py and networking.py. The first has 2 classes, one for the ball and another for the players. The second file also has two classes, one for the OSC server andthe other for the client.
