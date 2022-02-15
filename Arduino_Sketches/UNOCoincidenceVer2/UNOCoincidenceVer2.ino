/*
This script will use an Arduino UNO to log concidences

Plan:
Need a PPS signal
Need serial-coms with the GPS
Need timer1 to timestamp events AND count between PPS

Remember to re-enable the sifwareserial in the library.
 */
#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>


SoftwareSerial mySerial(6, 5); //TX,RX
Adafruit_GPS GPS(&mySerial);

volatile unsigned long nanosecond;
volatile unsigned long second;
int minute;
int hour;

volatile bool logging = true; // True when we log concidences
volatile bool Fix = false; // True when the GPS has confimed a fix
volatile bool Ready=false;

volatile unsigned long cyclesInSecond; //clockcycles we had last second
volatile unsigned long overflowCounter=0; // counter for timer0 overflows
volatile float clkSpeed=62.5; // clockspeed in ns

//For recording events:
volatile unsigned long EventNanosec=0;
volatile unsigned long EventSec=0;
volatile bool EventFlag = false;

volatile byte low; //For readout
volatile byte high;
volatile int combined;

unsigned long timer1TOP=65536;

//Pinning:
int PPSPin = 2;
//Signal on D8
//GPS on hardware serial.


void setup() {
  
  Serial.begin(38400);
  GPS.begin(9600);//Start connection to GPS
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY); //Tell GPS we only need basic data
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate

  Serial.println("Waiting for GPS Fix");


  //setup pin8 (PORTB0) to be the interrupt pin:
  DDRB = 0; //Set as input
  

  //Set timer1 up for interrupting:
  TCCR1A = 0;// set entire TCCR1A register to 0
  TCCR1B = 0;// same for TCCR1B
  TCNT1  = 0;//initialize counter value to 0
  // Set CS10 bit for no prescaler
  TCCR1B |= (1 << CS10);   
  // enable external interrupt
  TIMSK1 |= bit(ICIE1);

  // enable timer overflow interrupt
  TIMSK1 |= (1 << TOIE1);
  
  pinMode(PPSPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PPSPin),PPS,RISING);

  sei();
  
}

void loop() {
  //main loop
  if(Fix == false) {
    Startup();
  } else if (logging) {
    Normal();
  } else {
    //Do nothing
  }
}

void Startup(){
  //Run this until we have time from GPS  
  
  char c = GPS.read(); //read GPS module
  if (GPS.newNMEAreceived()) {//If we received something, parse it
    if (!GPS.parse(GPS.lastNMEA()))   // this also sets the newNMEAreceived() flag to false
      return;  // we can fail to parse a sentence in which case we should just wait for another
  }

  if (((GPS.day != 0) and (Ready==false)) and (GPS.fix==true)){ //The GPS sent us a time, so get ready to start!
    nanosecond=0;
    minute=GPS.minute; //save time we got
    second=GPS.seconds;
    hour=GPS.hour;

    Serial.print("GPS Fix obtained at;");
    printTime(second,nanosecond,true);
    
    Ready=true; // Go into normal mode when next second ticks
  }
  
}

void Normal(){
  //Normal operating loop
  CheckPulse(); //Check if we need to print about an event
  
  StopLoggingCheck(); //Check if we should stop
}


void CheckPulse(){
  //Check if we had an event 
  if (EventFlag){
    Serial.print("Coincidence;");
    printTime(EventSec,EventNanosec,false);
    EventFlag=false; //lower flag
  }
}

void StopLoggingCheck(){
  //This we call to check if we were told to stop
  if (Serial.available() > 0) {
    // read the incoming byte:
    char message = Serial.read();
    if (message=='s'){
      Serial.print("Stopping logging session;");
      nanosecond=NanosecondsNow();
      printTime(second,nanosecond,true);
      logging=false;
    }
   }
}

unsigned long NanosecondsNow(){
  return (overflowCounter * timer1TOP + TCNT1)*clkSpeed;
}

void PPS(){//interrupt from GPS 
  cyclesInSecond = overflowCounter * timer1TOP + TCNT1; //How many cycles passed since last PPS event
  clkSpeed=1e9/cyclesInSecond; //Recompute clockspeed (in ns)
  //Serial.println(clkSpeed);
  overflowCounter=0; //reset overflow, we entered new second
  second = second +1;
  if (Ready==true and Fix==false){
    Fix=true; // we can enter normal mode
    EventFlag=false; // Disregard earlier events
  }
  
}

ISR(TIMER1_OVF_vect){ //Run the ISR for Timer1 overflow
  overflowCounter=overflowCounter+1; //Increment counter
}

ISR(TIMER1_CAPT_vect){ //ISR for events on the pin
  if (EventFlag==false){ //only record if we have lowered flag from last event
    low = ICR1L; //read bytes form register, order is important
    high = ICR1H;
    combined = 0;
    combined = (high<<8) | low;
    
    EventNanosec = (overflowCounter * timer1TOP + combined)*clkSpeed; //#cylces times clockspeed (since second ticked over)
    EventSec=second;
    EventFlag=true; //raise flag
  }
}

void printTime(unsigned long sec,unsigned long nanosec, bool printDate){
  //Prints the time, and perhaps the date also
  //Idea is to never increment min and hr variables, instead we compute what we need to print from sec and nanosec
  int PrintNanosecond=nanosec%1000;
  int PrintMicrosecond=(nanosec%1000000)/1000;
  int PrintMillisecond=(nanosec%1000000000)/1000000;
  int PrintSecond=(sec+nanosec/1000000000)%60;
  int PrintMinute=(minute+(sec+nanosec/1000000000)/60)%60;
  int PrintHour=hour+(minute+(sec+nanosec/1000000000)/60)/60;

  //print in chosen format:
  if (PrintHour < 10) { Serial.print('0'); }
  Serial.print(PrintHour, DEC); Serial.print(':');
  if (PrintMinute < 10) { Serial.print('0'); }
  Serial.print(PrintMinute, DEC); Serial.print(':');
  if (PrintSecond < 10) { Serial.print('0'); }
  Serial.print(PrintSecond, DEC); Serial.print('.');
  
  if (PrintMillisecond < 10) {
    Serial.print("00");
  } else if (PrintMillisecond > 9 && PrintMillisecond < 100) {
    Serial.print("0");
  }
  Serial.print(PrintMillisecond); Serial.print(':');
  
  if (PrintMicrosecond < 10) {
    Serial.print("00");
  } else if (PrintMicrosecond > 9 && PrintMicrosecond < 100) {
    Serial.print("0");
  }
  Serial.print(PrintMicrosecond); Serial.print(':');

  if (PrintNanosecond < 10) {
    Serial.print("00");
  } else if (PrintNanosecond > 9 && PrintNanosecond < 100) {
    Serial.print("0");
  }
  Serial.print(PrintNanosecond); Serial.print(':');
  
  if (printDate){
    Serial.print(";Date:");
    Serial.print(GPS.day, DEC); Serial.print('/');
    Serial.print(GPS.month, DEC); Serial.print("/20");
    Serial.println(GPS.year, DEC);
  } else {
    Serial.println(";");
  }
}
