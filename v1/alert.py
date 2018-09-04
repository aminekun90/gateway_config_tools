import time
import logging
global COMMS
class Alert(object):
    def __init__(self, name, alarm, trigger, threshold, device, sensor, value, state="TRIGGERED", timestamp=None):
        self.name = name
        self.trigger = trigger
        self.threshold = threshold
        self.device = device
        self.sensor = sensor 
        self.value = value
        self.state = state  # TRIGGERED, RECOVERED
        self.timestamp = timestamp or int(time.time())
        self.alarm = alarm

    def send(self):
        logging.info("Sending alert!!!!!!!!!!!!!")
        if not COMMS:
            logging.error("No COMMS configured")
            return
        data = {"alert": {
                "name": self.name,
                "alarm": self.alarm,
                "trigger": self.trigger,
                "threshold": self.threshold,
                "device": self.device,
                "sensor": self.sensor,
                "value": self.value,
                "timestamp": self.timestamp,
                "state": self.state
            }}
        COMMS.alert(data)
