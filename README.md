# Pond-Temp-Display

## Background

Raspberry Pico network receiver and display codebase for the Pico based temperature sender solution, see.

This code base will receive UDP broadcast packets containing temperature data from the aforementioned sender and plot average probe data and housing data on a Waveshare 1.28 inch display.

The display background will change depending on the water temperature observed.
```
 < 15c = Blue
 > 15c < 24c = Green
 > 24c = Red
```
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

### Setup 
These instructions enable the software on the required hardware. 
These instructions do not cover the physical installation or support for the hardware.

### Pico

* Clone the repo from here to your location system
* Modify file wifi_settings.txt with your WiFi SSID and password
* Download the latest Pico W uf2 file
* Press and hold the BOOTSEL button
* Connect the Pico to your computer via the appropriate USB cable, after connecting release the BOOTSEL button, the PICO should be mounted to your filesystem.
* Copy all the cloned files including the modified wifi_settings.txt to the Pico.
* Copy the uf2 file, the Pico should restart, and the timer automatically starts.

#### Wifi Settings
Example wifi settings file, also includes UDP broadcast port and buffer, these values shouldn't require changing unless you have a conflict.  Source should be updated if you modify.
```
{
    "wifi_ssid": "your_ssid",
    "wifi_password": "password_value",
    "data_port": 5007,
    "buffer_size": 1024
}
```
