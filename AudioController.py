from pycaw.pycaw import AudioUtilities
import time
from enum import Enum
import ctypes

class Modes(Enum):
    APPLICATION = 1
    OUTPUT_DEVICE = 2
    #INPUT_DEVICE = 3

class InputDevices(Enum):
    Plantronics = 1
    Microphone = 2

class AudioController:
    def __init__(self, device_switcher_lib:str):
        self.sessions = []
        self.active_session = 0
        self.interface = None
        self.device_switcher = ctypes.cdll.LoadLibrary(device_switcher_lib)     
        self.device_switcher.Init()

        self.output_devices = {}
        self.read_output_devices()
        
        self.modes = Modes
        self.input_devices = InputDevices
        
        self.active_mode = self.modes.APPLICATION
        self.active_input_device = self.input_devices.Microphone
    
    def read_output_devices(self):
        self.device_switcher.Export_Device_Config()
        config_file = open("config", "r")

        output_device_index = 0
        for output_device in config_file:
            self.output_devices[output_device_index] = output_device
            output_device_index += 1

        #print(self.output_devices)
        self.active_device_index = self.device_switcher.Get_Active_Device_Id()
        self.active_device_name = self.output_devices[self.active_device_index]
        print("Active Output Device: {}".format(self.active_device_name))

    def update_sessions(self):
        #print("Active Session ID : {}".format(self.active_session))
        self.sessions = AudioUtilities.GetAllSessions()
        for session in self.sessions:
            if not session.Process:
                self.sessions.remove(session)
        #print(self.sessions)
    
        self.interface = self.sessions[self.active_session].SimpleAudioVolume

    def mute(self):
        self.update_sessions()
        if self.sessions[self.active_session].Process:
            self.interface.SetMute(1, None)

    def unmute(self):
        self.update_sessions()
        interface = self.sessions[self.active_session].SimpleAudioVolume
        if self.sessions[self.active_session].Process:
            interface.SetMute(0, None)

    def process_volume(self):
        self.update_sessions()
        if self.sessions[self.active_session].Process:
            return self.interface.GetMasterVolume()

    def set_volume(self, decibels):
        self.update_sessions()
        volume = self.process_volume()
        if self.sessions[self.active_session].Process:
            volume = min(1.0, max(0.0, decibels))
            self.interface.SetMasterVolume(volume, None)

    def decrease_volume(self, decibels):
        self.update_sessions()
        volume = self.process_volume()
        if self.sessions[self.active_session].Process:
            volume = max(0.0, volume - decibels)
            self.interface.SetMasterVolume(volume, None)

    def increase_volume(self, decibels):
        self.update_sessions()
        volume = self.process_volume()
        if self.sessions[self.active_session].Process:
            volume = min(1.0, volume + decibels)
            self.interface.SetMasterVolume(volume, None)
    
    # direction can only be 1 or -1
    def switch_active_session(self, direction):
        if direction == 1 and self.active_session < len(self.sessions) - 1:
            self.active_session += 1
        elif direction == -1 and self.active_session != 0:
            self.active_session -= 1
        print("Active Session: {}".format(self.sessions[self.active_session]))

    # direction can only be 1 or -1
    def switch_audio_input_device(self, direction):
        current_input_device_idx = list(InputDevices).index(self.active_input_device)
        next_input_device_idx = (current_input_device_idx + direction) % len(InputDevices)
        self.active_input_device = list(InputDevices)[next_input_device_idx]

    # direction can only be 1 or -1
    def switch_audio_output_device(self, direction):
        if direction == 1 and self.active_device_index < (len(self.output_devices) - 1):
            self.active_device_index += 1
        elif direction == -1 and self.active_device_index != 0:
            self.active_device_index -= 1

        #print(self.active_device_index)
        self.device_switcher.Set_Output_Device_By_Index(self.active_device_index)
        self.active_device_name = self.output_devices[self.active_device_index]
        print("Active Output Device: {}".format(self.active_device_name))

    def switch_mode(self):
        current_mode_idx = list(Modes).index(self.active_mode)
        next_mode_idx = (current_mode_idx + 1) % len(Modes)
        self.active_mode = list(Modes)[next_mode_idx]
        #print(current_mode_idx)
        print("Active Mode {}".format(self.active_mode.name))

def main():
    audio_controller = AudioController(r"C:\Users\Gjergji\Repos\VolCtrl\OutputDeviceSwitcher\OutputDeviceSwitcher\build\Debug\OutputDeviceSwitcher.dll")
    audio_controller.active_session = 1
    audio_controller.set_volume(1.0)
    audio_controller.mute()
    time.sleep(1)
    audio_controller.decrease_volume(0.25)
    audio_controller.increase_volume(0.05)
    audio_controller.unmute()
    audio_controller.switch_audio_output_device(1)
    time.sleep(1)
    audio_controller.switch_audio_output_device(-1)
    

if __name__ == "__main__":
    main()