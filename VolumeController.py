from pycaw.pycaw import AudioUtilities
import time
from enum import Enum
import ctypes

class Modes(Enum):
    APPLICATION = 1
    OUTPUT_DEVICE = 2
    #INPUT_DEVICE = 3

class VolumeController:
    def __init__(self):
        self.apps = []
        self.active_app_index = 0
        self.active_app_index_interface = None

        self.modes = Modes
        self.active_mode = self.modes.APPLICATION
        self.update_apps()
    
    def update_apps(self):
        self.apps = AudioUtilities.GetAllapps()
        for session in self.apps:
            if not session.Process:
                self.apps.remove(session)

        self.active_app_index_interface = self.apps[self.active_app_index].SimpleAudioVolume

    def mute(self):
        self.update_apps()
        if self.apps[self.active_app_index].Process:
            self.active_app_index_interface.SetMute(1, None)

    def unmute(self):
        self.update_apps()
        active_app_index_interface = self.apps[self.active_app_index].SimpleAudioVolume
        if self.apps[self.active_app_index].Process:
            active_app_index_interface.SetMute(0, None)

    def process_volume(self):
        self.update_apps()
        if self.apps[self.active_app_index].Process:
            return self.active_app_index_interface.GetMasterVolume()

    def set_volume(self, decibels):
        self.update_apps()
        volume = self.process_volume()
        if self.apps[self.active_app_index].Process:
            volume = min(1.0, max(0.0, decibels))
            self.active_app_index_interface.SetMasterVolume(volume, None)

    def decrease_volume(self, decibels):
        self.update_apps()
        volume = self.process_volume()
        if self.apps[self.active_app_index].Process:
            volume = max(0.0, volume - decibels)
            self.active_app_index_interface.SetMasterVolume(volume, None)

    def increase_volume(self, decibels):
        self.update_apps()
        volume = self.process_volume()
        if self.apps[self.active_app_index].Process:
            volume = min(1.0, volume + decibels)
            self.active_app_index_interface.SetMasterVolume(volume, None)
    
    # direction can only be 1 or -1
    def change_active_app_index(self, direction):
        if direction == 1 and self.active_app_index < len(self.apps) - 1:
            self.active_app_index += 1
        elif direction == -1 and self.active_app_index != 0:
            self.active_app_index -= 1
        print("Active Application: {}".format(self.apps[self.active_app_index]))


    def switch_mode(self):
        current_mode_idx = list(Modes).index(self.active_mode)
        next_mode_idx = (current_mode_idx + 1) % len(Modes)
        self.active_mode = list(Modes)[next_mode_idx]
        print("Active Mode {}".format(self.active_mode.name))
