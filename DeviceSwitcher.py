import ctypes
import time

lib_device_switcher = ctypes.cdll.LoadLibrary(r"C:\Users\Gjergji\Repos\VolCtrl\OutputDeviceSwitcher\OutputDeviceSwitcher\out\build\x64-debug\OutputDeviceSwitcher.dll")
lib_device_switcher.Init()
lib_device_switcher.ListAudioDevices()
#lib_device_switcher.SetDefaultAudioPlaybackDeviceByIndex(3)
device_count = lib_device_switcher.GetAudioDeviceCount()
print("Device Count {}".format(device_count))
lib_device_switcher.SetDefaultAudioPlaybackDeviceByIndex(1)
time.sleep(2)
lib_device_switcher.SetDefaultAudioPlaybackDeviceByIndex(3)
lib_device_switcher.Deinit()
