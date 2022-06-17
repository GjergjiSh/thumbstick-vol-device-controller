import serial
import time

class Interpreter:
    def __init__(self, serial_port, serial_baudrate=115200, serial_timeout=.1):
        self.arduino = serial.Serial(port=serial_port, baudrate=serial_baudrate, timeout=serial_timeout)
        self.moved_up = False
        self.moved_down = False
        self.moved_right = False
        self.moved_left = False
        self.clicked = False

    def read_input(self) -> str:
        if self.arduino.is_open:
            input = self.arduino.readline().decode("utf-8")
            input = input.split("-")
            
            if len(input) == 1:
                return
        
            #print(input)
            return input


    def interpret_input(self, input:list) -> None:
        if input == None:
            return

        x = int(input[0])
        y = int(input[1])
        z = input[2]

        if x > 600:
            self.moved_left = True
        elif x < 400:
            self.moved_right = True
        else:
            self.moved_left = False
            self.moved_right = False

        if y > 600:
            self.moved_down = True
        elif y < 400:
            self.moved_up = True
        else:
            self.moved_down = False
            self.moved_up = False
        
        if z == "0\r\n":
            self.clicked = True
        else:
            self.clicked = False

    def close(self) -> None:
        self.arduino.close()

if __name__ == "__main__":
    interpreter = Interpreter(serial_port="COM3")
    while interpreter.arduino.is_open:
        input = interpreter.read_input()
        interpreter.interpret_input(input)
        print("Down {} - Up {} - Left {} - Right {} - Click {}"
            .format(interpreter.moved_down, 
                    interpreter.moved_up, 
                    interpreter.moved_left, 
                    interpreter.moved_right, 
                    interpreter.clicked))