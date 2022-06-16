const int X_PIN = 3;  // X Achsis
const int Y_PIN = 1;  // Y Achsis
const int SW_PIN = 2; // Button

String x_input;
String y_input;
String z_input;
String serial_output;

void setup() {
  Serial.begin(115200);
}

void loop() {
  x_input = String(analogRead(X_PIN));
  y_input = String(analogRead(Y_PIN));
  z_input = String(analogRead(SW_PIN));
  serial_output = x_input +"-"+ y_input +"-"+ z_input;

  Serial.println(serial_output);
  delay(100);
}
