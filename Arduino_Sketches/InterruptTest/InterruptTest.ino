int interruptPin = 13; //Pin we get interrupt signal from

volatile bool Event = false; // did we have event?
volatile unsigned long EventCounter = 0; //time of event
volatile unsigned long EventCounter2 = 0; //time of event

void setup() {
  pinMode(interruptPin, INPUT);

  attachInterrupt(digitalPinToInterrupt(interruptPin),event,RISING); //make interrupt possible

  Serial.begin(9600);
  Serial.println(digitalRead(interruptPin));
}

void loop() {
  if (Event==true){
    Event=false;
    Serial.println(EventCounter2-EventCounter);
  }
  
}

void event(){ //This we do if interrupt is called
  EventCounter=micros();
  Event=true;
  delay(1);
  EventCounter2=micros(); 
}
//Above is to test if the micros() counter stil runs inside the interrupt, and it seems that it does!
