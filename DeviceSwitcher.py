import ctypes
import time

lib_device_switcher = ctypes.cdll.LoadLibrary(r"C:\Users\Gjergji\Repos\VolCtrl\OutputDeviceSwitcher\OutputDeviceSwitcher\out\build\x64-debug\OutputDeviceSwitcher.dll")
lib_device_switcher.Init()
lib_device_switcher.List_Output_Devices()
#lib_device_switcher.Set_Output_Device_By_Index(3)
device_count = lib_device_switcher.Get_Output_Device_Count()
print("Device Count {}".format(device_count))
#lib_device_switcher.Set_Output_Device_By_Index(1)
#time.sleep(2)
#lib_device_switcher.Set_Output_Device_By_Index(3)
lib_device_switcher.Deinit()
