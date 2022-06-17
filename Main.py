import AudioController as AC
import SerialInterpreter as SI

if __name__ == "__main__":
    audio_controller = AC.AudioController()
    interpreter = SI.Interpreter("COM3")

    while interpreter.arduino.is_open:
       audio_controller.update_sessions()

       serial_input = interpreter.read_input()
       interpreter.interpret_input(serial_input)
       if interpreter.moved_right:
           if audio_controller.active_session < len(audio_controller.sessions) - 1:
               audio_controller.active_session += 1
               print(
                   audio_controller.sessions[audio_controller.active_session])
       elif interpreter.moved_left:
           if audio_controller.active_session != 0:
               audio_controller.active_session -= 1
               print(
                   audio_controller.sessions[audio_controller.active_session])
       elif interpreter.moved_up:
           audio_controller.increase_volume(0.1)
       elif interpreter.moved_down:
           audio_controller.decrease_volume(0.1)
