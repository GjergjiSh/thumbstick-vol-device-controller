from email.mime import audio
import AudioController as AC
import SerialInterpreter as SI

if __name__ == "__main__":
    audio_controller = AC.AudioController(r"C:\Users\Gjergji\Repos\VolCtrl\OutputDeviceSwitcher\OutputDeviceSwitcher\build\Debug\OutputDeviceSwitcher.dll")
    interpreter = SI.Interpreter("COM3")
    audio_controller.update_sessions()

    while interpreter.arduino.is_open:

       serial_input = interpreter.read_input()
       interpreter.interpret_input(serial_input)
       
       if interpreter.clicked:
        audio_controller.switch_mode()
       
       if audio_controller.active_mode == AC.Modes.APPLICATION:
        if interpreter.moved_down:
            audio_controller.decrease_volume(0.1)
        elif interpreter.moved_up:
            audio_controller.increase_volume(0.1)
        elif interpreter.moved_left:
            audio_controller.switch_active_session(-1)
        elif interpreter.moved_right:
             audio_controller.switch_active_session(1)
       elif audio_controller.active_mode == AC.Modes.OUTPUT_DEVICE:
        if interpreter.moved_left:
            audio_controller.switch_audio_output_device(-1)
        elif interpreter.moved_right:       
             audio_controller.switch_audio_output_device(1)

    audio_controller.device_switcher.Deinit()