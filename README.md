# Garden-Monitor

In my Garden I have an Arduino Nano connected to a range of sensors that give me environmental data about my Chilli plants. The Nano is then connected via USB/Serial to a Raspberry Pi 3 (RPi). The image below shows the installed setup in an old box, the only external sensors are the Soil Temperature and Soil Moisture sensors. I just want to point out that this setup is not the best. Firstly the sensors are all on a breadboard, but the worst issue is that the RPi has to be installed with the Nano and is heavily underutilised. Having this work with an NodeMCU or something similar would be the best, I could also then install multiple sensors and have the data sent over wifi to the RPi then upload. Anyway, this works so v0.1 it is :-)

<p float="center">
  <img src="https://github.com/astrobenhart/Garden-Monitor/blob/master/images/installed1.jpg" width="425" />
  <img src="https://github.com/astrobenhart/Garden-Monitor/blob/master/images/installed2.jpg" width="425" /> 
</p>

The RPi sends messages to the Nano every 5 minutes to query each sensor one at a time, stores the sensor data in a SQLite database then uploads this to GitHub. The RPi used to also produce plots of the last 2 hours of data but that was unstable and was eventually halted. An example of this plot, and the data collected can be seen below.

![Plots](https://github.com/astrobenhart/Garden-Monitor/blob/master/plots/plots.png "Garden data plot")
