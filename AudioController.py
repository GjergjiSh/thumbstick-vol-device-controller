from email.mime import application
from pycaw.pycaw import AudioUtilities
import sounddevice as SD
import time
from enum import Enum

class Modes(Enum):
    APPLICATION = 1
    INPUT_DEVICE = 2
    OUTPUT_DEVICE = 3

class OutputDevices(Enum):
    LC32G5xT = 1
    Speakers = 2

class InputDevices(Enum):
    Plantronics = 1
    Microphone = 2

class AudioController:
    def __init__(self):
        self.sessions = []
        self.active_session = 0
        self.interface = None

        self.modes = Modes
        self.input_devices = InputDevices
        self.output_devices = OutputDevices
        
        self.active_mode = self.modes.APPLICATION
        self.active_output_device = self.output_devices.LC32G5xT
        self.active_input_device = self.input_devices.Microphone
    
        # self.registered_output_devices = {
        #     'LC32G5xT' : 8,
        #     'Speakers' : 4
        # }

        # self.registered_input_devices = {
        #     'Plantronics' : 1,
        #     'Microphone' : 2
        # }

        # self.active_output_device = "LC32G5xT"
        # self.active_input_device = "Microphone"

        # self.modes = ["Application", "Input Device", "Output Device"]
        # self.active_mode = self.modes[0]

    def update_sessions(self):
        self.sessions = AudioUtilities.GetAllSessions()
        for session in self.sessions:
            if not session.Process:
                self.sessions.remove(session)
    
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
    def switch_audio_input_device(self, direction):
        current_input_device_idx = list(InputDevices).index(self.active_input_device)
        next_input_device_idx = (current_input_device_idx + direction) % len(InputDevices)
        self.active_input_device = list(InputDevices)[next_input_device_idx]
        print(current_input_device_idx)
        print(self.active_input_device.name)

    def switch_audio_output_device(self, direction):
        current_output_device_idx = list(OutputDevices).index(self.active_output_device)
        next_output_device_idx = (current_output_device_idx + direction) % len(OutputDevices)
        self.active_output_device = list(OutputDevices)[next_output_device_idx]
        print(current_output_device_idx)
        print(self.active_output_device)

    def switch_mode(self):
        current_mode_idx = list(Modes).index(self.active_mode)
        next_mode_idx = (current_mode_idx + 1) % len(Modes)
        self.active_mode = list(Modes)[next_mode_idx]
        print(current_mode_idx)
        print(self.active_mode.name)
        
    # def switch_audio_output_device(self):
        # print(self.active_input_device)


def main():
    audio_controller = AudioController()
    audio_controller.active_session = 1
    audio_controller.set_volume(1.0)
    audio_controller.mute()
    time.sleep(1)
    audio_controller.decrease_volume(0.25)
    audio_controller.increase_volume(0.05)
    audio_controller.unmute()
    

if __name__ == "__main__":
    #main()
    audio_controller = AudioController()
    audio_controller.switch_audio_input_device()

