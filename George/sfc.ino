String str;
int incomingByte = 0;
unsigned long lastTime;
volatile int Signal; 
int pulsePin = 0;    
void setup() {
  Serial.begin(9600);
  pinMode(13,OUTPUT); 
  Serial.print("{INIT1#/");
  lastTime = 0;
  str = "";
}
char ch;
void loop() {
   incomingByte  = Serial.read();
   ch = char(incomingByte);
   if((ch != '/') && (incomingByte != -1) && (ch != '[')&& (ch != '{')&& (ch != '(')&& (ch != '#'))
   {
       str += ch;
   }
   else if((ch == '/') && (str.length() > 0))
   {
    //Serial.print(str);
    //Serial.print('/');
    if(str == "on") digitalWrite(13,HIGH);
    else if(str == "off") digitalWrite(13,LOW);
    else if(str == "time -s"){
      Serial.print("{working ");
      Serial.print(millis()/1000);
      Serial.print(" sec#/");
    }
    else if(str != ""){
      Serial.print("{Command not found: ");
      Serial.print(str);
      Serial.print("#/");
    }
    if((str == "on")||(str=="off"))
    {
      Serial.print("{13 pin: ");
      Serial.print(str);
      Serial.print("#/");
    }
    str = "";
  }
    if(millis() - lastTime >20){
    Signal = analogRead(pulsePin);
    Serial.print("[");
    Serial.print(millis());
    Serial.print("(");
    Serial.print(Signal);
    Serial.print("#/");
    lastTime = millis();
  }
}

/*  Автор: Georgy_Smith  */
/*  Изменен:   17.10.17  */

