import MainController as MC

if __name__ == "__main__":
    main_controller = MC.MainController(
        config_file_path="config",
        device_switcher_lib=r"C:\Users\Gjergji\Repos\VolCtrl\OutputDeviceSwitcher\OutputDeviceSwitcher\build\Debug\OutputDeviceSwitcher.dll",
        serial_port="COM3"
    )
   
    while main_controller.serial_interpreter.arduino.is_open:
        main_controller.handle_mode()
        main_controller.serial_interpreter.interpret_input()
        main_controller.handle_applications()
        main_controller.handle_output_devices()


    main_controller.deinit()