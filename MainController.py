import VolumeController as VC
import DeviceController as DC
import SerialInterpreter as SI
from enum import Enum


class Modes(Enum):
    APPLICATION = 1
    OUTPUT_DEVICE = 2
    #INPUT_DEVICE = 3


class MainController():
    def __init__(self, config_file_path, device_switcher_lib, serial_port):
        self.volume_controller = VC.VolumeController()
        self.device_controller = DC.DeviceController(
            device_switcher_lib=device_switcher_lib, config_file_path=config_file_path)
        self.serial_interpreter = SI.SerialInterpreter(serial_port=serial_port)

        self.modes = Modes
        self.active_mode = self.modes.APPLICATION

    def switch_mode(self):
        current_mode_idx = list(Modes).index(self.active_mode)
        next_mode_idx = (current_mode_idx + 1) % len(Modes)
        self.active_mode = list(Modes)[next_mode_idx]
        print("Active Mode {}".format(self.active_mode.name))

    def handle_mode(self):
        if self.serial_interpreter.clicked:
            self.switch_mode()

    def handle_applications(self):
        if self.active_mode == Modes.APPLICATION:
            if self.serial_interpreter.moved_down:
                self.volume_controller.decrease_volume(decibels=0.1)
            elif self.serial_interpreter.moved_up:
                self.volume_controller.increase_volume(decibels=0.1)
            elif self.serial_interpreter.moved_left:
                self.volume_controller.change_active_app_index(direction=1)
            elif self.serial_interpreter.moved_right:
                self.volume_controller.change_active_app_index(direction=-1)

    def handle_output_devices(self):
        if self.active_mode == Modes.OUTPUT_DEVICE:
            if self.serial_interpreter.moved_left:
                self.device_controller.switch_output_device(direction=-1)
            elif self.serial_interpreter.moved_right:
                self.device_controller.switch_output_device(direction=1)

    def deinit(self):
        self.device_controller.deinit()
        self.serial_interpreter.close()