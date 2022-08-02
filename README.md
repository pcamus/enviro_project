## Project with the enviro+ hat.

In this project I used a Raspberry Pi 3B board with an [enviro+](https://shop.pimoroni.com/products/enviro?variant=31155658457171) hat from Pimoroni and a [pms5003](https://github.com/m2mlorawan/datasheet/blob/master/plantower-pms5003-manual_v2-3.pdf) particle sensor.

This project was an opportunity to test the PyQt GUI toolkit and the Google sheet access from Python.

The GUI was designed with QtDesigner and and PyQt5 was used for the program. 

The program uses the relevant library modules for the sensors (see inside the main code).

*The GUI window is the following :*

![](enviro_gui.jpg)

The program uses 3 timers (QTimer objects) :

- 3 minutes timer for logging in gsheet (and reseting the sum of each measurement used in the averages).
- 10 seconds timer for data acquisition and averaging.
- 1 second timer to display the time in the status bar.

5 events are taken into account : the 3 timers events, the start recording button clicked event and the Quit command in the File menu

References : [QtDesigner by Michael Hermann](https://build-system.fman.io/qt-designer-download)

- [ ] To do : see if this PyQt5 program runs on PyQt6 (impossible to load the libraries for now (1/8/2022)).
- [x] To do : see how to use .ui file directly from Python without converting it before.

- [ ] Remaining problem : installation of PyQt5, whatever the version, on the Raspberry Pi (3B or 4) running Raspbian Bullseye doesn't work. Hopfully it was pre-installed in one of my older micro SD card (still Bullseye) and I was able run the program succesfuly. During my first attempts, two years ago, it worked without problem, but it was with the buster OS.
