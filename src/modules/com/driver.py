import serial
from config import config

config = config["serial"]


class SerialConnection:
    def __init__(self, **driver):
        self.port = config["port"]
        self.baudrate = config["baudrate"]
        self.parity = (
            serial.PARITY_NONE if config["parity"] == "None" else serial.PARITY_ODD
        )
        self.stopbits = (
            serial.STOPBITS_ONE if config["stopbits"] == 1 else serial.STOPBITS_TWO
        )
        self.bytesize = serial.EIGHTBITS
        self.timeout = config["timeout"]
        self.flow_control = config["flow-control"]
        self.ser = None

        self.password = driver["password"]
        self.username = driver["username"]

    def log_in(self):  # TODO: реализовать. (IMPORTANT NOT URGENT)
        with self as conn:
            print(type(conn), self.password, self.username)

    def __enter__(self):
        self.ser = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            parity=self.parity,
            stopbits=self.stopbits,
            bytesize=self.bytesize,
            timeout=self.timeout,
        )
        self.ser.xonxoff = self.flow_control["xonxoff"]
        self.ser.rtscts = self.flow_control["rtscts"]
        self.ser.dsrdtr = self.flow_control["dsrdtr"]
        self.ser.open()
        return self.ser

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.ser and self.ser.is_open:
            self.ser.close()
