import ctypes

class DeviceController:
    def __init__(self, device_switcher_lib:str, config_file_path:str):
        self.device_switcher = ctypes.cdll.LoadLibrary(device_switcher_lib)
        self.device_config_file = config_file_path
        self.device_switcher.Init()
        self.get_output_devices()
        self.get_active_output_device()

    def deinit(self):
        self.device_switcher.Deinit()

    def get_output_devices(self):
        self.device_switcher.Export_Device_Config()
        config_file = open(self.device_config_file, "r")

        self.output_devices = {}
        output_device_index = 0
        for output_device in config_file:
            self.output_devices[output_device_index] = output_device
            output_device_index += 1

        return self.output_devices

    def get_active_output_device(self) -> tuple:
        self.active_device_index = self.device_switcher.Get_Active_Device_Id()
        self.active_device_name = self.output_devices[self.active_device_index]
        self.active_device = (self.active_device_index, self.active_device_name)

        return self.active_device

        
    def switch_output_device(self, direction) -> tuple:
        if direction == 1 and self.active_device_index < (len(self.output_devices) - 1):
            self.active_device_index += 1
        elif direction == -1 and self.active_device_index != 0:
            self.active_device_index -= 1

        self.device_switcher.Set_Output_Device_By_Index(self.active_device_index)
        self.active_device_name = self.output_devices[self.active_device_index]
        self.active_device = (self.active_device_index, self.active_device_name)
        print("Active Output Device: {} {}".format(self.active_device_index, self.active_device_name))

        return (self.active_device)