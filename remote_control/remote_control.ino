#include "TimerOne.h"

#define READ_SENSOR_INTERVAL 1000UL  // периодичность вывода времени в Serial (1 cекунда)
#define SERIAL_SPEED 9600 // скорость работы Serial

int IN1 = 7; // Input1 подключен к выводу 7
int IN2 = 6;
int IN3 = 5;
int IN4 = 4;
int ENA = 9;
int ENB = 3;

unsigned int counter = 0;

const int numReadings = 3; // количество усредняемых элементов в массиве

int readings0[numReadings];      // the readings from the analog input
int readIndex0 = 0;              // the index of the current reading
int total0 = 0;                  // the running total
int average0 = 0;                // the average

int readings1[numReadings];      // the readings from the analog input
int readIndex1 = 0;              // the index of the current reading
int total1 = 0;                  // the running total
int average1 = 0;                // the average

char command = 'S';
char prevCommand = 'A';
int velocity = (4 + 1) * 10 + 100;   
// velocity = (command - 48 + 1) * 10 + 100;

unsigned long timer0 = 2000;  //Stores the time (in millis since execution started) 
unsigned long timer1 = 0;  //Stores the time when the last command was received from the phone

void docount()  // counts from the speed sensor
{
  counter++;  // increase +1 the counter value
}

void setup() {
  // задаем скорость работы ком-порта
  Serial.begin(SERIAL_SPEED);
  pinMode (ENA, OUTPUT);
  pinMode (IN1, OUTPUT);
  pinMode (IN2, OUTPUT);
  pinMode (ENB, OUTPUT);
  pinMode (IN4, OUTPUT);
  pinMode (IN3, OUTPUT);

  // обнуление массивов для хранения показаний с датчиков
  for (int thisReading0 = 0; thisReading0 < numReadings; thisReading0++) {
    readings0[thisReading0] = 0;
  }

  for (int thisReading1 = 0; thisReading1 < numReadings; thisReading1++) {
    readings1[thisReading1] = 0;
  }
}

int saveP0 = 0;
int cntSec0 = 0;
int saveP1 = 0;
int cntSec1 = 0;

const int wheel_diameter = 128;   // Диаметр колеса в мм

void loop()
{
  digitalWrite (IN2, LOW);
  digitalWrite (IN1, HIGH);
  digitalWrite (IN4, LOW);
  digitalWrite (IN3, HIGH);

  //// A  70
  // analogWrite(ENA, 180); // 64 - крутится // 63 почти всё уже
  //// B  88
  // analogWrite(ENB,  80); // 77 - не крутится // 79 начал крутится
  // ищем стабильное значение

  int sensorReading0 = digitalRead(A0);
  int sensorReading1 = digitalRead(A1);

  if (saveP0 != sensorReading0)
  {
    cntSec0 = cntSec0 + 1;
  }
  saveP0 = sensorReading0;

  if (saveP1 != sensorReading1)
  {
    cntSec1 = cntSec1 + 1;
  }
  saveP1 = sensorReading1;

  // периодически выводим millis() в Serial
  static unsigned long prevSensorTime = 0;
  if (millis() - prevSensorTime > READ_SENSOR_INTERVAL) {
    prevSensorTime = millis();

    // subtract the last reading:
    total0 = total0 - readings0[readIndex0];
    // read from the sensor:
    readings0[readIndex0] = cntSec0;
    // add the reading to the total:
    total0 = total0 + readings0[readIndex0];
    // advance to the next position in the array:
    readIndex0 = readIndex0 + 1;

    // if we're at the end of the array...
    if (readIndex0 >= numReadings) {
      // ...wrap around to the beginning:
      readIndex0 = 0;
    }
    average0 = total0 / numReadings;

    // subtract the last reading:
    total1 = total1 - readings1[readIndex1];
    // read from the sensor:
    readings1[readIndex1] = cntSec1;
    // add the reading to the total:
    total1 = total1 + readings1[readIndex1];
    // advance to the next position in the array:
    readIndex1 = readIndex1 + 1;

    // if we're at the end of the array...
    if (readIndex1 >= numReadings) {
      // ...wrap around to the beginning:
      readIndex1 = 0;
    }
    average1 = total1 / numReadings;
    int msec = 60 / 10;

    int rpm0 = average0 * msec;
    int rpm1 = average1 * msec;

    float velocity0 = rpm0 * 3.1416 * wheel_diameter * 60 / 1000000;
    float velocity1 = rpm1 * 3.1416 * wheel_diameter * 60 / 1000000;
    
/*
    Serial.print(rpm0);
    Serial.print(':');
    Serial.print(rpm1);
    Serial.print(" (rpm);    ");
    Serial.print(velocity0);
    Serial.print(':');
    Serial.print(velocity1);
    Serial.println(" (km/h)"); */

    cntSec0 = 0;
    cntSec1 = 0;
  }
  
  // https://sites.google.com/site/bluetoothrccar/home/3BluetoothModulesAndArduinoCode

  if (Serial.available() > 0) {
    timer1 = millis();
    prevCommand = command;
    command = Serial.read();
    //Change pin mode only if new command is different from previous.
    if (command != prevCommand) {
      //Serial.println(command);
      switch (command) {
        case 'W':
          //forward
          analogWrite(ENA, velocity); // 64 - крутится // 63 почти всё уже
          analogWrite(ENB, velocity); // 77 - не крутится // 79 начал крутится
          break;
        case 'A':
          //Left
          // A
            digitalWrite (IN2, LOW);
            digitalWrite (IN1, HIGH);
          // B
            digitalWrite (IN4, HIGH);
            digitalWrite (IN3, LOW);
          
          break;
        case 'S':
          //Backward

          digitalWrite (IN2, HIGH);
          digitalWrite (IN1, LOW);
          digitalWrite (IN4, HIGH);
          digitalWrite (IN3, LOW);
          
          break;
        case 'D':
          //Right
          //velocity = (3 + 1) * 10 + 100;
          // A
          digitalWrite (IN2, HIGH);
          digitalWrite (IN1, LOW);
          // B
          digitalWrite (IN4, LOW);
          digitalWrite (IN3, HIGH);          
          break;
        case ' ': //Stop
          //velocity = 0;
          analogWrite(ENA, 0); // 64 - крутится // 63 почти всё уже
          analogWrite(ENB, 0); // 77 - не крутится // 79 начал крутится
          break;
        default:  //Get velocity
          if (command == 'q') {
            velocity = 255;  //Full velocity
            //yellowCar.SetSpeed_4W(velocity);
          }
          else {
            //Chars '0' - '9' have an integer equivalence of 48 - 57, accordingly.
            if ((command >= 48) && (command <= 57)) {
              //Subtracting 48 changes the range from 48-57 to 0-9.
              //Multiplying by 25 changes the range from 0-9 to 0-225.
              if (command == 48)
              {
                velocity = 0;
              }
              else
              {
                velocity = (command - 48 + 1) * 10 + 100;
              }
              analogWrite(ENA, velocity); // 64 - крутится // 63 почти всё уже
              analogWrite(ENB, velocity); // 77 - не крутится // 79 начал крутится
            }
          }
      }
    }
  }
  else {
    timer0 = millis();  //Get the current time (millis since execution started).
    //Check if it has been 500ms since we received last command.
    if ((timer0 - timer1) > 500) {
      //More tan 500ms have passed since last command received, car is out of range.
      //Therefore stop the car and turn lights off.
      
      //yellowCar.Stopped_4W();
    }
  }


}
