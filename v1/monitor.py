import hashlib
import re
import os
import logging 
import time
from v1.sensor import SensorType
from six import string_types

DATA_FOLDER = "./data"
class Monitor:
    def __init__(self, name, alarm, device="any", sensor="any", triggers=None, retrigger=86400, **kw):
        """
        Monitor Definition

        :param str name: Name of the monitor
        :param str alarm: 
        :param str device: The device to monitor can be all, a device id
        """
        self.name = name
        if not isinstance(name, string_types) or not re.match(r"^[\w\s!\.'\"\-\?]+$", name):
            raise AttributeError("Invalid name")
        if not isinstance(device, string_types):
            raise AttributeError("Invalid device")
        self.device = device.lower()
        if not isinstance(sensor, string_types):
            raise AttributeError("Invalid sensor")
        self.sensor_name = sensor.upper()
        if not triggers or not isinstance(triggers, dict) or len(triggers.keys())<1:
            raise AttributeError("Invalid triggers")
        self.triggers = {k.lower(): v for k, v in triggers.items()}
        if not isinstance(retrigger, int) or retrigger < 0 or isinstance(retrigger, bool):
            raise AttributeError("Invalid retrigger")
        self.retrigger = retrigger
        self.alarm = alarm
        
    def serialize(self):
        return {
            'name':self.name,
            'device':self.device,
            'sensor_name':self.sensor_name,
            'retrigger':self.retrigger,
            'alarm':self.alarm,
            'triggers':self.triggers
        }


class Monitors(object):
    def __init__(self, *args):
        for arg in args:
            if not isinstance(arg, Monitor):
                raise AttributeError("All arguments must be of type Monitor")
        self.__monitors = list(args)

    def add(self, monitor):
        if not isinstance(monitor, Monitor):
            raise AttributeError("Invalid monitor, must be dict")
        self.__monitors.append(monitor)

    def __iter__(self):
        for monitor in self.__monitors:
            yield monitor

    def __len__(self):
        return len(self.__monitors)

    def check(self, sensor):
        """ Check sensor data on all monitors """
        if not isinstance(sensor, SensorType):
            raise AttributeError("Invalid sensor, must be of type Sensor")
        #logging.debug(self.__monitors)
        for monitor in self.__monitors:
            monitor.check(sensor)
