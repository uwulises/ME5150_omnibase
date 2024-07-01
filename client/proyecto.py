from controlClient import ControlClient
from streamClient import StreamClient

ip = "192.168.100.101"
camara = StreamClient(ip)
control = ControlClient(ip, 12345)

