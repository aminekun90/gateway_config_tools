

class Comms:

    name = "bc95"
    port = "/dev/ttyS4"
    udp_addr = "52.19.219.211"
    udp_port = 10000
    apn = "nb.inetd.gdsp"
    operator = "27201"
    band = 20

    def __init__(self, name, port, udp_addr, udp_port, apn, operator, band):
        self.name = name
        self.port = port
        self.udp_addr = udp_addr
        self.udp_port = udp_port
        self.apn = apn
        self.operator = operator
        self.band = band
    def serialize(self):
        return {
        'name':self.name,
        'port':self.port,
        'udp_addr':self.udp_addr,
        'udp_port':self.udp_port,
        'apn':self.apn,
        'operator':self.operator,
        'band':self.band
        }
