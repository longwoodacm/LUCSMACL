int outPin = 13;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(outPin, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0){
    char inByte = Serial.read();
    //Serial.println(inByte, DEC);
    if(inByte == '1'){
      digitalWrite(outPin, HIGH);
	    delay(1000);
	    digitalWrite(outPin, LOW);
    }/*else if(inByte == '0'){
      digitalWrite(outPin, LOW);
    }*/
  }
  delay(1000);
}
