import ctypes

lib_device_switcher = ctypes.cdll.LoadLibrary(r"C:\Users\Gjergji\Repos\VolCtrl\OutputDeviceSwitcher\OutputDeviceSwitcher\out\build\x64-debug\OutputDeviceSwitcher.dll")
lib_device_switcher.EnumerateAudioPlaybackDevices()