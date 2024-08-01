# Pond-Temp-Display

## Background

Raspberry Pico network receiver and display codebase for the Pico based temperature sender solution, see.

This code base will receive UDP broadcast packets containing temperature data from the aforementioned sender and plot average probe data and housing data on a Waveshare 1.28 inch display.

## Hardware Requirements
* Raspberry Pico W
* Waveshare 1.28-inch round touch display (https://www.waveshare.com/1.28inch-touch-lcd.htm)

### Hardware Connections
* VCC -> 3.3V
* GND -> GND
* MISO -> 12
* MOSI -> 11
* SCLK -> 10
* LCD_CS -> 9
* LCD_DC -> 14
* LCD_RST -> 8
* LCD_BL -> 15
* TP_SDA -> 6
* TP_SCL -> 7
* TP_INT -> 16
* TP_RST -> 17
