#include <Adafruit_GPS.h> // GPS Libraries
#include <SoftwareSerial.h>

SoftwareSerial mySerial(8, 7); //TX,RX
Adafruit_GPS GPS(&mySerial);

//Variables for time-keeping
int lastsec=0;
unsigned long microTimer_offset; //Used to store output of micros() command, for fine timing

//Variables for reading pulses
bool inPulse=false;
int readout;

void setup() {
  Serial.begin(19200);
  GPS.begin(9600);//Start connection to GPS
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY); //Tell GPS we only need basic data
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate
  
  pinMode(A0,INPUT); //Used to listen to coincidence module
}

void loop() {
  char c = GPS.read(); //read GPS module
  if (GPS.newNMEAreceived()) {//If we received something, parse it
    if (!GPS.parse(GPS.lastNMEA()))   // this also sets the newNMEAreceived() flag to false
      return;  // we can fail to parse a sentence in which case we should just wait for another
  }

  if (GPS.seconds!=lastsec){//We have reached a new second (so GPS.milliseconds will be 0)
    lastsec=GPS.seconds;
    microTimer_offset=micros();//Time offset (micros overflows after approx. 1 hr)
    //At moment of overflow will cause some strange timing
  }

  readout = analogRead(A0);//read pulse
  if (readout<600) { //We are in pulse
    if (inPulse==false) { //we just entered a pulse
      inPulse=true;
      Serial.print("Coincidence;");
      printTime(GPS,microTimer_offset);
    }
  } else {
    inPulse=false;
  }
  
}


void printTime(Adafruit_GPS GPS, unsigned long microTimer_offset){//Takes GPS as input along with internal timer and prints time to serial connection
  
  unsigned long microTimer=(micros()-microTimer_offset); //Compute microseconds since last second ticked over
  
  Serial.print("Time:"); //Note that this logs GMT
    if (GPS.hour < 10) { Serial.print('0'); }
    Serial.print(GPS.hour, DEC); Serial.print(':');
    if (GPS.minute < 10) { Serial.print('0'); }
    Serial.print(GPS.minute, DEC); Serial.print(':');

    int second = GPS.seconds+microTimer/1000000;
    
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
