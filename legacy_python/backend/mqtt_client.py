import paho.mqtt.client as mqtt
import threading

class AmbiLumMQTTClient:
    def __init__(self, broker, port, topic_lux, on_lux_update_callback):
        self.broker = broker
        self.port = port
        self.topic_lux = topic_lux
        self.on_lux_update_callback = on_lux_update_callback
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.is_connected = False
        self.thread = None

    def start(self):
        """Starts the MQTT loop in a separate thread to avoid blocking the UI."""
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def _run_loop(self):
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_forever()
        except Exception as e:
            print(f"MQTT Connection Error: {e}")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            self.is_connected = True
            self.client.subscribe(self.topic_lux)
        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
        if msg.topic == self.topic_lux:
            try:
                lux_value = float(msg.payload.decode())
                if self.on_lux_update_callback:
                    self.on_lux_update_callback(lux_value)
            except ValueError:
                pass
