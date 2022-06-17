from pycaw.pycaw import AudioUtilities
import time


class AudioController:
    def __init__(self):
        self.sessions = []
        self.active_session = 0

    def update_sessions(self):
        self.sessions = AudioUtilities.GetAllSessions()

    def mute(self, process_name):
        self.update_sessions()
        for session in self.sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == process_name:
                interface.SetMute(1, None)
                print(process_name, "has been muted.")  # debug

    def unmute(self, process_name):
        self.update_sessions()
        for session in self.sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == process_name:
                interface.SetMute(0, None)
                print(process_name, "has been unmuted.")  # debug

    def process_volume(self, process_name):
        self.update_sessions()
        for session in self.sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == process_name:
                print("Volume:", interface.GetMasterVolume())  # debug
                return interface.GetMasterVolume()

    def set_volume(self, process_name, decibels):
        self.update_sessions()
        volume = self.process_volume(process_name)
        for session in self.sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == process_name:
                # only set volume in the range 0.0 to 1.0
                volume = min(1.0, max(0.0, decibels))
                interface.SetMasterVolume(volume, None)
                print("Volume set to", volume)  # debug

    def decrease_volume(self, process_name, decibels):
        self.update_sessions()
        volume = self.process_volume(process_name)
        for session in self.sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == process_name:
                # 0.0 is the min value, reduce by decibels
                volume = max(0.0, volume - decibels)
                interface.SetMasterVolume(volume, None)
                print("Volume reduced to", volume)  # debug

    def increase_volume(self, process_name, decibels):
        self.update_sessions()
        volume = self.process_volume(process_name)
        for session in self.sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == process_name:
                # 1.0 is the max value, raise by decibels
                volume = min(1.0, volume + decibels)
                interface.SetMasterVolume(volume, None)
                print("Volume raised to", volume)  # debug


def main():
    audio_controller = AudioController()
    audio_controller.set_volume("chrome.exe", 1.0)
    audio_controller.mute("chrome.exe")
    audio_controller.decrease_volume("chrome.exe", 0.25)
    audio_controller.increase_volume("chrome.exe", 0.05)
    audio_controller.unmute("chrome.exe")


if __name__ == "__main__":
    main()