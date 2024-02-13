void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  unsigned int val = 65536 - touchRead(13);
  Serial.println(val);
  delay(10);
}
