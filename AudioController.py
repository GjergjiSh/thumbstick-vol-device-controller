from pycaw.pycaw import AudioUtilities
import time

class AudioController:
    def __init__(self):
        self.sessions = []
        self.active_session = 0
        self.interface = None

    def update_sessions(self):
        self.sessions = AudioUtilities.GetAllSessions()
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
    main()