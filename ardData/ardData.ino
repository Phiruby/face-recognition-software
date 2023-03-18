int trigPin=2;
int echoPin=3;

float waveTime;
float distance;
float speedSound=0.000331; //meter per microsecond
void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);
pinMode(trigPin,OUTPUT);
pinMode(echoPin,INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
digitalWrite(trigPin,LOW);
delayMicroseconds(10);
digitalWrite(trigPin,HIGH);
delayMicroseconds(10);
digitalWrite(trigPin,LOW);
waveTime=pulseIn(echoPin,HIGH);
//Wave time is time for wave to travel both ways
distance=speedSound*waveTime/2.;
Serial.println(distance);
delay(1000);

}
