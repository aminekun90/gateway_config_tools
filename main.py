import logging
from v1.gateway import Gateway
from v1.comms import Comms
from v1.sensor import SensorType
from v1.monitor import Monitor


logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    comms = Comms(name='bc95', port='/dev/ttyS4', udp_addr='52.19.219.211',
                  udp_port=10000, apn="nb.inetd.gdsp", operator="27201", band=20)
    sensor_TMP = SensorType('TEMP', 1800, "U", "U", "GAUGE",
                            ["AVERAGE", "MIN", "MAX"])
# - name: VIBRATION
# step: 300
# rra: ["AVERAGE", "MAX"]
# minimum: U
# maximum: U
# dst: GAUGE

    sensor_vib = SensorType(name='VIBRATION', step=300, rra=["AVERAGE", "MAX"])
    sensor_shock = SensorType(name='SHOCK', step=1800, rra=["AVERAGE", "MIN", "MAX"])
#     # for this specific device with ID as below alert if VIBRATION was above 5G
#   - name: SHOCK
#     alarm: 7b14432c-18a1-4c8b-8d78-76580bcf2210
#     device: all
#     sensor: SHOCK
#     triggers:
#       above: 0.0
    monitor_TMP = Monitor('Temperature outside threshold', 1, 'all', sensor='TEMP', triggers={
        'above': 10.0, 'below': -20.0}, retrigger=86400)
    monitor_shock = Monitor('SHOCK', '7b14432c-18a1-4c8b-8d78-76580bcf2210', 'all', sensor='SHOCK', triggers={
        'above': 0.0}, retrigger=86400)

    monitor_vib = Monitor(name='Extreme vibration detected!', alarm='cdb1c9ff-9de0-4def-8c74-a2e396894c9c',
                          device='all', sensor='VIBRATION', triggers={'above': 20.0})
    gateway = Gateway('MDhlOWFmODgtOWYwZC00MzRkLTg5MjUtNTY2MTZmYTJhOTQ3OmMyMDA0YmVjNTAyNTQ4YTg4YmE0ZDhkZjAxY2NjMzAwYzUxNzhmODlhZWU3NGU5N2FhNzhiNzhlMjNmMTIyYjU=',
                      comms, "0 0 * * *", 1440, sensors=[sensor_TMP, sensor_vib,sensor_shock], devices=[], monitors=[monitor_TMP, monitor_vib,monitor_shock])
    gateway.generate_config_file('data/config.yml')
