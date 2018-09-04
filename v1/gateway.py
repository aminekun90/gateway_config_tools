
import yaml
import logging
from v1.comms import Comms
from v1.sensor import SensorType, SensorTypes
from v1.monitor import Monitor, Monitors

MONITORS = None
COMMS = None
SENSORS = None


class Gateway:
    # api_token = None
    # send_update_cron = 1440
    # comms = Comms()
    # send_update_cron = "0 0 * * *"
    # send_update_interval = 1440
    # sensors = []
    # devices = []  # Should we add devices list ?? ToDo confirm this
    # monitors = []

    def __init__(self, api_token, comms, send_update_cron, send_update_interval, sensors, devices=[], monitors=[]):
        """
        Gateway definition

        """
        self.api_token = api_token
        self.comms = comms
        self.send_update_cron = send_update_cron
        self.send_update_interval = send_update_interval
        self.sensors = []
        self.devices = []
        self.monitors = []
        if not sensors or not isinstance(sensors, list):
            raise ValueError("'sensors' is not a list or an empty one")
        for sensor in sensors:
            self.sensors.append(sensor)

        if not isinstance(devices, list):
            raise ValueError("'devices' is not a list")
        # for device in devices:
        #     self.devices.add(Device(**device))

        if not isinstance(monitors, list):
            raise ValueError("'devices' is not a list")
        for monitor in monitors:
            self.monitors.append(monitor)

    def generate_config_file(self,file_path='data/config.yml'):
        """
        generate a file
        """
        with open(file_path, 'w') as yaml_file:
            sensors_data = [sensor.serialize() for sensor in self.sensors]
            monitors_data = [monitor.serialize() for monitor in self.monitors]

            data = {
                "api_token": self.api_token,
                "comms": self.comms.serialize(),
                "send_update_cron": self.send_update_cron,
                "send_update_interval": self.send_update_interval,
                "sensors": sensors_data,
                "monitors": monitors_data

            }
            if self.devices:
                data['devices'] = self.devices
            yaml.dump(
                data, yaml_file, default_flow_style=False
            )
            logging.info('Configration file created')

    # def read_config_file(self, config_file):
        # global COMMS
        # global SENSORS
        # global MONITORS

        # config = yaml.load(open(config_file, 'r'))
        # self.sensors = config.get('sensors')
        # logging.info("Setting up SensorTypes")
        # if not self.sensors or not isinstance(self.sensors, list):
        #     raise ValueError("'sensors' list is missing in config file")

        # for sensor in self.sensors:
        #     logging.debug(sensor)
        #     SENSORS.add(SensorType(**sensor))
        # logging.info("Loading Monitors")
        # self.monitors = config.get("monitors") or []
        # if not isinstance(self.monitors, list):
        #     raise ValueError("'monitors' list is missing in config file")

        # for monitor in self.monitors:
        #     logging.debug(monitor)
        #     MONITORS.add(Monitor(**monitor))
