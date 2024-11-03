# wind_speed

Pseudo Wind Speed Measurement for Raspberry Pi (Wind Velocity)

## M5Stack Technology's M5 ENV III Sensor
It has two sensor devices, SHT30 and QMP6988.
This software calculates a wind speed from the temperature sensors in them.

## The Method of Pseudo Wind Speed Calculation

A heater on the SHT30 chip is turned on when measuring the temperature.
It increase the temperature value by a few degrees.
If wind will blow to it, the temperature value might be decreased depending on the wind speed.
So, it can calculate a wind speed value from a heated temperature sensor and a normal one.

## GitHub Pages (This Document)

* [https://git.bokunimo.com/wind_speed/](https://git.bokunimo.com/wind_speed/)

by <https://bokunimo.net>
