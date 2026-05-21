import requests

class WLEDClient:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.base_url = f"http://{self.ip_address}/json/state"
        
    def _send_request(self, data):
        """Helper to send JSON to WLED."""
        if not self.ip_address:
            return False
            
        try:
            response = requests.post(self.base_url, json=data, timeout=2)
            return response.status_code == 200
        except Exception as e:
            print(f"WLED Request Error: {e}")
            return False

    def toggle_power(self, on: bool):
        """Turn WLED on or off."""
        return self._send_request({"on": on})
        
    def set_brightness(self, brightness: int):
        """Set brightness from 0 to 255."""
        brightness = max(0, min(255, int(brightness)))
        return self._send_request({"bri": brightness})
        
    def set_color(self, hex_color: str):
        """Set WLED color using a HEX string like #FF0000."""
        try:
            if hex_color.startswith("#"):
                hex_color = hex_color[1:]
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            
            return self._send_request({
                "seg": [{"col": [[r, g, b]]}]
            })
        except Exception:
            return False
