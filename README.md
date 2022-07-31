## Project with the enviro+ hat.

In this project I used a Raspberry Pi 4 board with an [enviro+](https://shop.pimoroni.com/products/enviro?variant=31155658457171) hat from Pimoroni and a [pms5003](https://github.com/m2mlorawan/datasheet/blob/master/plantower-pms5003-manual_v2-3.pdf) particle sensor.

This project was an opportunity to test the PyQt GUI toolkit and the Google sheet access from Python.

The GUI was designed with QtDesigner and PyQt 5. 

The program uses relevant library modules for the sensors (see inside the main code).

*The GUI window is the following :*
![](enviro_gui.jpg)

The program uses 3 timers (QTimer objects) :

- 3 minutes timer for logging in gsheet.
- 10 seconds timer for data acquisition and averaging.
- 1 second timer to display the time in the staus bar.

5 events are taken into account : the 3 timers events, the start recording button clicked event and the Quit command in the File menu

References : [QtDesigner by Michael Hermann](https://build-system.fman.io/qt-designer-download)

- [ ] To do : see if this PyQt5 program runs on PyQt6.
- [ ] To do : see how to use .ui file directly from Python without converting it before.
