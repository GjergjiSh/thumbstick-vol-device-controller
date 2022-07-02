from email.mime import audio
import VolumeController as VC
import DeviceController as DC
import SerialInterpreter as SI

if __name__ == "__main__":
    volume_controller = VC.VolumeController()
    device_controller = DC.DeviceController(device_switcher_lib=r"C:\Users\Gjergji\Repos\VolCtrl\OutputDeviceSwitcher\OutputDeviceSwitcher\build\Debug\OutputDeviceSwitcher.dll",
                                            config_file_path="config")

    serial_interpreter = SI.SerialInterpreter(serial_port="COM3")
    volume_controller.update_apps()

    while serial_interpreter.arduino.is_open:
       serial_interpreter.interpret_input()

       if serial_interpreter.clicked:
        volume_controller.switch_mode()

       if volume_controller.active_mode == VC.Modes.APPLICATION:
        if serial_interpreter.moved_down:
            volume_controller.decrease_volume(decibels=0.1)
        elif serial_interpreter.moved_up:
            volume_controller.increase_volume(decibels=0.1)
        elif serial_interpreter.moved_left:
            volume_controller.change_active_app_index(direction=1)
        elif serial_interpreter.moved_right:
            volume_controller.change_active_app_index(direction=-1)

       elif volume_controller.active_mode == VC.Modes.OUTPUT_DEVICE:
        if serial_interpreter.moved_left:
            device_controller.switch_output_device(direction=-1)
        elif serial_interpreter.moved_right:
            device_controller.switch_output_device(direction=1)

    device_controller.deinit()
