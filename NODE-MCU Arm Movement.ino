#include <Servo.h>
Servo servoG;
Servo servoF;
Servo servoR;
Servo servoT;

void setup() {
servoG.attach(D8); servoG.write(70); // Grab (70-0)
servoF.attach(D5); servoF.write(50); // Front-Back (50-180)
servoR.attach(D6); servoR.write(90); // Rotation (0-180)
servoT.attach(D7); servoT.write(180);// Tilt (80-180)

Serial.begin(9600);
Serial.setTimeout(10);
}

// Main loop is here
void loop() {
while(Serial.available() == 0){} // do nothing
String serialData = Serial.readString(); // R90T180F50G70 demo serialData

servoR.write(getPosR(serialData));
servoT.write(getPosT(serialData));
servoF.write(getPosF(serialData));
servoG.write(getPosG(serialData));
}
// ========== servo movement ============
// Rotation
int getPosR(String data){
  data.remove(data.indexOf("T"));
  data.remove(data.indexOf("R"),1);

  return data.toInt();
}
// Tilt
int getPosT(String data){
  data.remove(0, data.indexOf("T")+1);
  data.remove(data.indexOf("F"));

  return data.toInt();
}
// Forward
int getPosF(String data){
  data.remove(0, data.indexOf("F")+1);
  data.remove(data.indexOf("G"));

  return data.toInt();
}
// Grab
int getPosG(String data){
  data.remove(0, data.indexOf("G")+1);

  return data.toInt();
}
