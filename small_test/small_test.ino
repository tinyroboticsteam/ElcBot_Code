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

void setup() {
  // задаем скорость работы ком-порта
  Serial.begin(SERIAL_SPEED);
  pinMode (ENA, OUTPUT);
  pinMode (IN1, OUTPUT);
  pinMode (IN2, OUTPUT);
  pinMode (ENB, OUTPUT);
  pinMode (IN4, OUTPUT);
  pinMode (IN3, OUTPUT);
}

void loop()
{
  // периодически выводим millis() в Serial
  static unsigned long prevSensorTime = 0;
  if (millis() - prevSensorTime > READ_SENSOR_INTERVAL) {

    prevSensorTime = millis();
    if (myflag == 1)
    {
      randNumber = random(300);
      Serial.print(command);
      Serial.println(randNumber);
    }
    if (myflag == 2)
    {
      randNumber = 0;
      Serial.print(command);
      Serial.println(randNumber);
    }
    
  }

  if (Serial.available() > 0) {
    timer1 = millis();
    prevCommand = command;
    command = Serial.read();
    // Выполняем условие, только если новая команда, отличается от предыдущей

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
      prevCommand = ' ';

    }
  }
}

