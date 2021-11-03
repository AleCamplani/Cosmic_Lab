#include <Adafruit_GPS.h> // GPS Libraries
#include <SoftwareSerial.h>

SoftwareSerial mySerial(8, 7); //TX,RX
Adafruit_GPS GPS(&mySerial);

//Variables for time-keeping
int lastsec=0;
unsigned long microTimer_offset; //Used to store output of micros() command, for fine timing

//Variables for reading pulses
volatile bool Event = false; // did we have event?
volatile unsigned long EventTime = 0; //time of event
int interruptPin = 13; //Pin we get interrupt signal from

//Variables for making sure we have GPS fix
bool GPSFix=false;

//For closing logging session
bool Logging = true; //To keep track of logging
char message;

//For startup
bool FirstGPSContact = false;

void setup() {
  Serial.begin(19200);
  GPS.begin(9600);//Start connection to GPS
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY); //Tell GPS we only need basic data
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate
  
  pinMode(interruptPin, INPUT); //Used to listen to coincidence module

  attachInterrupt(digitalPinToInterrupt(interruptPin),event,RISING); //make interrupt possible
  
  Serial.println("Waiting for GPS Fix");
}

void loop() {
  char c = GPS.read(); //read GPS module
  if (GPS.newNMEAreceived()) {//If we received something, parse it
    FirstGPSContact = true;
    if (!GPS.parse(GPS.lastNMEA()))   // this also sets the newNMEAreceived() flag to false
      return;  // we can fail to parse a sentence in which case we should just wait for another
  }

  if (GPS.seconds!=lastsec){//We have reached a new second (so GPS.milliseconds will be 0)
    lastsec=GPS.seconds;
    microTimer_offset=micros();//Time offset (micros overflows after approx. 1 hr)
    //At moment of overflow will cause some strange timing
  }
  if (FirstGPSContact==true){
    if ((int)GPS.fix==1){ //check if we have fix
      if (GPSFix==false){
        Serial.print("GPS Fix obtained at;");
        printTime(GPS,microTimer_offset,micros());
      }
      GPSFix=true;
    } else {
      if (GPSFix==true){
        Serial.print("GPS Fix lost at;");
        printTime(GPS,microTimer_offset,micros());
      }
      GPSFix=false;
    }
    if (GPSFix==true and Logging){ //only if we have fix, will we do logging
      CheckPulse();  
    } else {
      Event=false; //Disregard any events if we are not logging data
    }
  
    //Code for checking if we should stop logging:
    if (Serial.available() > 0) {
      // read the incoming byte:
      message = Serial.read();
      if (message=='s'){ //corresponds to single 's' character, since we send as soon as we press button on computer in Putty
        Serial.print("Stopping logging session;");
        printTime(GPS,microTimer_offset,micros());
        Logging=false;
      }
    }  
  }
}


void CheckPulse(){
  if (Event==true){ //An interrupt raised the event-flag
    Event=false; //lower flag
    Serial.print("Coincidence;");
    printTime(GPS,microTimer_offset,EventTime);
  }
}

void event(){ //function called when we have interrupt, cannot return anything or receive anything
  EventTime=micros(); //Note time of interrupt
  Event=true; //Raise flag
  
}

void printTime(Adafruit_GPS GPS, unsigned long microTimer_offset, unsigned long now){//Takes GPS as input along with internal timer and prints time to serial connection
  
  unsigned long microTimer=(now-microTimer_offset); //Compute microseconds since last second ticked over
  
  Serial.print("Time:"); //Note that this logs GMT
    if (GPS.hour < 10) { Serial.print('0'); }
    Serial.print(GPS.hour, DEC); Serial.print(':');

    int second = (GPS.seconds+microTimer/1000000)%60;
    int minute = GPS.minute+(GPS.seconds+microTimer/1000000)/60;
    
    if (minute < 10) { Serial.print('0'); }
    Serial.print(minute, DEC); Serial.print(':');

    
    
    if (second < 10) { Serial.print('0'); }
    Serial.print(second, DEC); Serial.print('.');
    int millisecond = (microTimer%1000000)/1000;
    int microsecond = microTimer%1000;
    
    if (millisecond < 10) {
      Serial.print("00");
    } else if (millisecond > 9 && millisecond < 100) {
      Serial.print("0");
    }
    Serial.print(millisecond); Serial.print(':');
    
    if (microsecond < 10) {
      Serial.print("00");
    } else if (microsecond > 9 && microsecond < 100) {
      Serial.print("0");
    }
    Serial.print(microsecond);
    
    Serial.print(";Date:");
    Serial.print(GPS.day, DEC); Serial.print('/');
    Serial.print(GPS.month, DEC); Serial.print("/20");
    Serial.println(GPS.year, DEC);
}
