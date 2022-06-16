import serial
import time
import AudioController

class Interpreter:
    moved_up : bool
    moved_down : bool
    clicked : bool

    def __init__(self, serial_port, serial_baudrate=115200, serial_timeout=0):
        self.arduino = serial.Serial(port=serial_port, baudrate=serial_baudrate, timeout=serial_timeout)
        self.arduino.open()

    def read_input(self) -> str:
        if self.arduino.is_open:
            input = self.arduino.readline().decode("utf-8")
            print(input)

    def close(self) -> None:
        self.arduino.close()

if __name__ == "__main__":
    interpreter = Interpreter(serial_port="COM3")
    while interpreter.arduino.is_open:
        interpreter.read_input()