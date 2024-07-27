// This code listens for serial commands from the Python script to control the fan
int fanPin = 9; // Pin connected to the transistor controlling the fan
int fanSpeed = 0; // Variable to store fan speed

void setup() {
  pinMode(fanPin, OUTPUT);
  Serial.begin(9600); // Start serial communication at 9600 baud rate
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read(); // Read the command sent from the Python script

    if (command == 'O') {
      fanSpeed = 255; // Turn fan on
    } else if (command == 'F') {
      fanSpeed = 0; // Turn fan off
    } else if (command == 'U') {
      fanSpeed = min(fanSpeed + 51, 255); // Increase fan speed
    } else if (command == 'D') {
      fanSpeed = max(fanSpeed - 51, 0); // Decrease fan speed
    }

    analogWrite(fanPin, fanSpeed); // Set fan speed
  }
}
