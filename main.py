# Pond Temp receiver
# PICO W Build
# ------------------------------------
from wifi import *
from touch_LCD import *
import json
import os


WIFI_SETTINGS_FILE = 'wifi_settings.txt'
BLINE1 = ["Pond", 30, 66, 3, "white"]
BLINE2 = ["Temp", 44, 96, 3, "white"]
BLINE3 = ["Monitor", 65, 126, 3, "white"]
BLINE4 = ["Mark Rodman", 65, 197, 1, "white"]
PARRAY = ["*", 100, 180, 3, "white"]
WIFI_HARDWARE_BOOT_DELAY = 2
BOOT_SPLASH_DELAY = 3

HIGH_TEMP = 24
HIGH_BG_COLOUR = "red"
GOOD_TEMP = 15
GOOD_BG_COLOUR = "green"
LOW_BG_COLOUR = "blue"


def receive_udp_broadcast(port=None, buffer_size=None):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Allow the socket to reuse the address
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to all available interfaces and the specified port
    sock.bind(('', port))
    print(f"Listening for UDP broadcasts on port {port}...")
    while True:
        # Receive data from the socket
        data, address = sock.recvfrom(buffer_size)
        data_json = json.loads(data)
        if len(data_json) > 0:
            # Let's update the display here
            sock.close()
            return data_json


def bg_temp_colour(temp):
    """
    Function to generate background colour string based on current
    pond temperature. 
    """
    temp = int(temp)
    if temp > HIGH_TEMP:
        return HIGH_BG_COLOUR
    elif temp > GOOD_TEMP:
        return GOOD_BG_COLOUR
    else:
        return LOW_BG_COLOUR


def main():  
    # Setup Waveshare screen.
    LCD = LCD_1inch28()
    LCD.set_bl_pwm(65535)
    Touch = Touch_CST816T(mode=1, LCD=LCD)
    
    # Bootscreen
    Touch.ControlScreen(LCD, text_array=[BLINE1, BLINE2, BLINE3, BLINE4], back_colour='blue')
    
    time.sleep(BOOT_SPLASH_DELAY)  # boot delay, without wifi hardware isn't ready
    point = False   # Toggle for display
    
    # Get Wifi setting from file
    try:
        with open(WIFI_SETTINGS_FILE, 'r') as file:
            wifi_json = json.load(file)
    except Exception as e:
        print(e)
        Touch.ControlScreen(LCD, text_array=[
                            ["Error: Wifi Settings", 50, 60, 1, "white"],
                            [str(e), 6, 120, 1, "white"]], back_colour="red")
        
    # dynamically define kv based on wifi input file
    # keys should be wifi_ssid, wifi_password, buffer_size, and port
    # see READ.me
    for key, value in wifi_json.items():
        globals()[key] = value
    
    wifi = PicoWiFi(wifi_ssid, wifi_password)
    networks = wifi.scan_networks()
    time.sleep(WIFI_HARDWARE_BOOT_DELAY)
    
    if wifi.check_SSID(wifi_ssid, wifi.networks):
        print("WiFi SSID present")       
        if wifi.connect():
            Touch.ControlScreen(LCD, text_array=[
                ["WiFi", 75, 66, 3, "white"],
                ["Connected", 10, 96, 3, "white"],
                [wifi_ssid, 30, 145, 2, "white"],
                [f"{wifi.get_ip()}", 30, 170, 2, "white"]], back_colour='green')
            print("Wi-Fi connected successfully!")
            print(f"IP Address: {wifi.get_ip()}")
            
            while 1:
                data_json = receive_udp_broadcast(port=data_port, buffer_size=buffer_size)
                for entry in data_json:
                # Check if the entry has a 'type' key and if it's value is 'avg_probe_reading'
                    if entry.get('type') == 'avg_probe_reading':
                        avg_probe_reading =  (entry['value'])
                for entry in data_json:
                    if entry.get('sensor_placement') == 'Pump housing':
                        ph_reading = (entry['centrigrade'])
                        
                        if point is False:
                            PARRAY[4] = "white"
                            point = True
                        else:
                            PARRAY[4] = "green"
                            point = False
                        
                        Touch.ControlScreen(LCD, text_array=[
                            [str(int(ph_reading)), 105, 30, 2, "white"],
                            [str(int(avg_probe_reading)), 30, 80, 12, "white"],
                            PARRAY
                             ], back_colour=bg_temp_colour(avg_probe_reading))
                    else:
                        pass

        else:
            print("it didn't connect")

if __name__ == '__main__':
    main()