#define SERIAL_SPEED 38400 // скорость работы последовательного порта
#define READ_SENSOR_INTERVAL 500UL  // периодичность вывода времени в Serial (1 cекунда)

int IN1 = 7; // Input1 подключен к выводу 7
int IN2 = 6;
int IN3 = 5;
int IN4 = 4;
int ENA = 9;
int ENB = 3;

char command     = 'S';
char prevCommand = 'A';
int velocity = (4 + 1) * 10 + 100; // коэффициент заполнения ШИМ

unsigned long timer0 = 2000; // Перехме Stores the time (in millis since execution started)
unsigned long timer1 = 0;    //Stores the time when the last command was received from the phone

long randNumber;
long myflag = 0;

//////////////////////////

const int numReadings = 3; // количество усредняемых элементов в массиве

int readings0[numReadings];      // the readings from the analog input
int readIndex0 = 0;              // the index of the current reading
int total0 = 0;                  // the running total
int average0 = 0;                // the average

int readings1[numReadings];      // the readings from the analog input
int readIndex1 = 0;              // the index of the current reading
int total1 = 0;                  // the running total
int average1 = 0;                // the average

//unsigned long timer0 = 2000;  //Stores the time (in millis since execution started) 
//unsigned long timer1 = 0;  //Stores the time when the last command was received from the phone

unsigned int counter = 0;

void docount()  // counts from the speed sensor
{
  counter++;  // increase +1 the counter value
}

int saveP0 = 0;
int cntSec0 = 0;
int saveP1 = 0;
int cntSec1 = 0;

const int wheel_diameter = 128;   // Диаметр колеса в мм

/////////////////////////

void setup() {
  // задаем скорость работы ком-порта
  Serial.begin(SERIAL_SPEED);
  pinMode (ENA, OUTPUT);
  pinMode (IN1, OUTPUT);
  pinMode (IN2, OUTPUT);
  pinMode (ENB, OUTPUT);
  pinMode (IN4, OUTPUT);
  pinMode (IN3, OUTPUT);
///////////////////////////////////
  // обнуление массивов для хранения показаний с датчиков
  for (int thisReading0 = 0; thisReading0 < numReadings; thisReading0++) {
    readings0[thisReading0] = 0;
  }

  for (int thisReading1 = 0; thisReading1 < numReadings; thisReading1++) {
    readings1[thisReading1] = 0;
  }  
}

void loop()
{

/////////////////////////////////////////////////////////////////////////
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
  
/////////////////////////////////////////////////////////////////////////
  
  // периодически выводим millis() в Serial
  static unsigned long prevSensorTime = 0;
  if (millis() - prevSensorTime > READ_SENSOR_INTERVAL) {

    prevSensorTime = millis();

/////////////////////////////////////////////////////////////////////////

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
    
    cntSec0 = 0;
    cntSec1 = 0;
/////////////////////////////////////////////////////////////////////////

    if (myflag == 1)
    {
      Serial.print(velocity0);
      Serial.print(":");
      Serial.print(velocity1);
    }
    if (myflag == 2)
    {
      Serial.print("0.00:0.00");
    }
    
  }

  if (Serial.available() > 0) {
    timer1 = millis();
    if (prevCommand != 'x')
        prevCommand = command;
        
    command = Serial.read();
    // Выполняем условие, только если новая команда, отличается от предыдущей

    // для отладки:
    /*Serial.print(command);
    Serial.print(":");
    Serial.println(prevCommand);*/

    if ((command == 'W') || (command == 'A') || (command == 'S') || (command == 'D') || (command == ' ') )
      myflag = 1;
      
    if (command == ' ') 
    // тут наверное нужен код, который отправляет 0 в виде скорости
      myflag = 2;

    if (command != prevCommand) {
      switch (command) {
        case 'W':
          // Вперёд
          analogWrite(ENA, 0);
          analogWrite(ENB, 0);
          delay(20);
          // Смена направления вращения колёс
          digitalWrite (IN2, LOW);
          digitalWrite (IN1, HIGH);
          digitalWrite (IN4, LOW);
          digitalWrite (IN3, HIGH);
          // Установка скважности ШИМ
          analogWrite(ENA, velocity);
          analogWrite(ENB, velocity);


          break;
        case 'A':
          // Налево
          analogWrite(ENA, 0);
          analogWrite(ENB, 0);
          delay(20);
          // Мотор A
          digitalWrite (IN2, LOW);
          digitalWrite (IN1, HIGH);
          // Мотор B
          digitalWrite (IN4, HIGH);
          digitalWrite (IN3, LOW);

          analogWrite(ENA, velocity);
          analogWrite(ENB, velocity);

          break;
        case 'S':
          // Назад
          analogWrite(ENA, 0);
          analogWrite(ENB, 0);
          delay(20);

          digitalWrite (IN2, HIGH);
          digitalWrite (IN1, LOW);
          digitalWrite (IN4, HIGH);
          digitalWrite (IN3, LOW);

          analogWrite(ENA, velocity);
          analogWrite(ENB, velocity);

          break;
        case 'D':
          // Направо

          analogWrite(ENA, 0);
          analogWrite(ENB, 0);
          delay(20);
          // A
          digitalWrite (IN2, HIGH);
          digitalWrite (IN1, LOW);
          // B
          digitalWrite (IN4, LOW);
          digitalWrite (IN3, HIGH);

          analogWrite(ENA, velocity);
          analogWrite(ENB, velocity);

          break;
        case ' ': // Остановка робота
          //velocity = 0;
          analogWrite(ENA, 0);
          analogWrite(ENB, 0);

          break;
        default:  // Обработка полученного значения мощности
          // Символ '0' - '9' по таблице ASCII имеет код 48 - 57.
          if ((command >= 48) && (command <= 57)) {
            // Вычитаем 48 из полученного кода символа и
            // получаем число в диапазоне от 0 до 9.
            if (command == 48)
            {
              velocity = 0;
            }
            else
            {
              velocity = (command - 48 + 1) * 10 + 100;
            }
            analogWrite(ENA, velocity);
            analogWrite(ENB, velocity);             
          }
      }
    } else
    {

    }
  }
  else {
    timer0 = millis();  // Получение текущего времени
    // Проверка на время отправки последней команды:
    // если прошло более секунды, робот останавливается
    if ((unsigned long)(timer0 - timer1) > 20000) {

      analogWrite(ENA, 0);
      analogWrite(ENB, 0);
      prevCommand = 'x';

    }
  }
}

