# Garden-Monitor

In my Garden I have an Arduino Nano connected to a range of sensors that give me environmental data about my Chilli plants. The Nano is then connected via USB/Serial to a Raspberry Pi 3 (RPi). The image below shows the installed setup in an old box, the only external sensors are the Soil Temperature and Soil Moisture sensors.

<p float="left">
  <img src="https://github.com/astrobenhart/Garden-Monitor/blob/master/images/installed1.jpg" width="100" />
  <img src="https://github.com/astrobenhart/Garden-Monitor/blob/master/images/installed2.jpg" width="100" /> 
</p>

![install1](https://github.com/astrobenhart/Garden-Monitor/blob/master/images/installed1.jpg "installation 1") | ![install2](https://github.com/astrobenhart/Garden-Monitor/blob/master/images/installed2.jpg "installation 2")

The RPi sends messages to the Nano every 5 minutes to query each sensor one at a time, stores the sensor data in a SQLite database then uploads this to GitHub. The RPi used to also produce plots of the last 2 hours of data but that was unstable and was eventually halted. An example of this plot, and the data collected can be seen below.

![Plots](https://github.com/astrobenhart/Garden-Monitor/blob/master/plots/plots.png "Garden data plot")
