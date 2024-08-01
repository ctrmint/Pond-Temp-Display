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
        self.networks = None

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
    
    
    def connect(self):
        print(f"Connecting to {self.ssid}...")
        self.wlan.connect(self.ssid, self.password)
        max_tries = 1
        while max_tries < 11:
            status = self.wlan.status()
            if status < 0 or status >= 3:
                break
            max_tries += 1
            print(f'Waiting for connection, status: {status}')
            time.sleep(1)
        return self.is_connected()
    
    def disconnect(self):
        self.wlan.disconnect()
        print("Disconnected from Wi-Fi.")
        return

    def check_SSID(self, ssid=None, networks=None):
        """
        Check to see if the SSID is available,
        """
        found = False
        for net in networks:
            if net[0].decode('utf-8') == ssid:
                found = True
        return found
    
    def scan_networks(self, debug=False):
        """
        Scan for networks
        """
        self.networks = self.wlan.scan()
        if debug:
            if len(self.networks) > 0:
                for net in self.networks:
                    ssid = net[0].decode('utf-8')
                    print(f"SSID: {ssid}, Signal Strength: {net[3]}")
        return self.networks

    def get_ip(self):
        return self.wlan.ifconfig()[0]