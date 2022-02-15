int readout;
int detections =0;

bool inPulse=false;

unsigned long t1;
unsigned long t2;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Beginning");

  pinMode(A0,INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  readout = analogRead(A0);
  if (readout<600) {
    Serial.println(readout);
    if (inPulse==false) { //we just entered a pulse
      t1=micros(); //time where we entered a pulse
      detections=detections+1;
      inPulse=true;
      Serial.println("Total Detections: "+String(detections));
    }
      
  } else {
    if (inPulse==true){ //We just exited
      t2=micros();
      Serial.println(t2-t1);//print puls elength in microseconds
    }
    inPulse=false;
  }
  
}
