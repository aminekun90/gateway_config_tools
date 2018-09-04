
import logging
from six import string_types
DAY_SECONDS = 60*60*24
MAX_STEP = 6 * 60 * 60  # 6hrs seems like a good max step for now
import re
class SensorType:

    def __init__(self, name, step, minimum="U", maximum="U", dst="GAUGE", rra=None, **kw):
        """
        Sensor definition

        :param str name: name of the sensor
        :param int step: sensor step (in seconds)
        :param str minimum: minimum value for the value, "U" for undefined
        :param str maximum: maximum value for the value, "U" for undefined
        :param str dst: data source type, can be GAUGE, COUNTER, ABSOLUTE or DERIVED
        :param list rra: list of round robin archive types, can be AVERAGE, MIN, MAX or LAST
        """
        self.name = name
        if not isinstance(name, string_types) or not re.match(r"^[a-zA-Z]+$", name):
            raise AttributeError("Invalid name")
        if isinstance(step, str):
            try:
                step = int(step)
            except:
                raise AttributeError("step must be an integer")
        if not isinstance(step, int):
            raise AttributeError("step must be an integer")
        self.step = step
        if not isinstance(step, int) or step < 1 or step > MAX_STEP or isinstance(step, bool):
            raise AttributeError("step must be an integer > 1")
        self.min = minimum
        self.max = maximum
        if self.min != "U" and not isinstance(self.min, (int, float)) or isinstance(self.min, bool):
            raise AttributeError("minimum must be a number or 'U'")
        if self.max != "U" and not isinstance(self.max, (int, float)) or isinstance(self.max, bool):
            raise AttributeError("maximum must be a number or 'U'")
        self.dst = dst
        if dst not in ["GAUGE", "COUNTER", "ABSOLUTE", "DERIVED"]:
            raise AttributeError("Invalid dst, must be one of: GAUGE, COUNTER, ABSOLUTE or DERIVED")
        self.rra = rra or ["AVERAGE"]
        if not isinstance(self.rra, list):
            raise AttributeError("rra must be a list containing one or more of: AVERAGE, MIN, MAX, LAST")
        for value in self.rra:
            if value not in ["AVERAGE", "MIN", "MAX", "LAST"]:
                raise AttributeError("rra must be a list containing one or more of: AVERAGE, MIN, MAX, LAST")    

    def __repr__(self):
        return self.name
    def serialize(self):
        return {
            'name':self.name,
            'step':self.step,
            'rra':self.rra,
            'maximum':self.max,
            'minimum':self.min,
            'dst':self.dst
        }
    @property
    def rra_defs(self):
        return [
            "RRA:{}:0.5:{}:{}".format(
                rra, 1, int(DAY_SECONDS / self.step)
            ) for rra in self.rra
        ]

class SensorTypes(object):
    def __init__(self, *args):
        for arg in args:
            if not isinstance(arg, SensorType) or arg.name in self.__dict__:
                raise AttributeError("every argument must be an instance of SensorType")
        self.__sensors = {arg.name: arg for arg in args}

    def add(self, sensor):
        if not isinstance(sensor, SensorType):
            raise AttributeError("Invalid sensor")
        if repr(sensor) in self.__sensors:
            raise AttributeError("Sensor is already added")
        self.__sensors[sensor.name] = sensor

    # def all(self):
    #     return self.__sensors

    def get(self, name):
        return self.__getattr__(name)

    def __getattr__(self, name):
        if not isinstance(name, string_types):
            logging.debug("wrong type {}".format(type(name)))
            raise AttributeError("sensor not defined")
        if name in self.__sensors:
            return self.__sensors[name]
        logging.debug("wrong name {}".format(name))
        raise AttributeError("sensor not defined")
