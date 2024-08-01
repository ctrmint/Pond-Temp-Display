import socket, json
import network
import time
   

class PicoWiFi():
    """
    A class for Wifi connectivity on the Pico.
    """
    def __init__(self, ssid: str, password: str):
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

    def connect(self):
        print(f"Connecting to {self.ssid}...")
        self.wlan.connect(self.ssid, self.password)
        max_wait = 10
        while max_wait > 0:
            status = self.wlan.status()
            if status < 0 or status >= 3:
                break
            max_wait -= 1
            print(f'Waiting for connection, status: {status}')
            time.sleep(1)
        return self.is_connected()

    def is_connected(self):
        status = self.wlan.status()
        if status == 3:
            print('Connected')
            print('Network config:', self.wlan.ifconfig())
            return True
        else:
            self._handle_connection_failure(status)
            return False

    def _handle_connection_failure(self, status):
        if status == -1:
            print('Wi-Fi connection failed: Connection failed')
        elif status == -2:
            print('Wi-Fi connection failed: No AP found')
        elif status == -3:
            print('Wi-Fi connection failed: Wrong password')
        else:
            print(f'Wi-Fi connection failed with status code: {status}')
        return

    def disconnect(self):
        self.wlan.disconnect()
        print("Disconnected from Wi-Fi.")
        return

    def scan_networks(self):
        print("Scanning for networks...")
        networks = self.wlan.scan()
        for net in networks:
            ssid = net[0].decode('utf-8')
            print(f"SSID: {ssid}, Signal Strength: {net[3]}")
        return networks

    def get_ip(self):
        return self.wlan.ifconfig()[0]