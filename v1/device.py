
import uuid

class Device:
    id = None
    name = ""
    connection_type = ""
    description = ""
    maintenance = False
    send_update_cron = ""
    status = ""
    is_gateway = False
    gateway_id = ""
    def __init__(self,id=uuid.uuid4(),name,connection_type,description,maintenance,send)
