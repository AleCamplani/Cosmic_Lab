#include <Adafruit_GPS.h> // GPS Libraries
#include <SoftwareSerial.h>

SoftwareSerial mySerial(8, 7); //TX,RX
Adafruit_GPS GPS(&mySerial);

int Readout=0; // To store readout value
int inputpin = 2; // Pin we read from

int prevValue; // Vaæue we compare to, to check for change

bool Logging = true; //To keep track of logging
char message;

bool Start=true;

unsigned long microTimer_offset; //Used to store output of micros() command, for fine timing

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200); // Start serial connection for logging, speed from GPS example.
  delay(2000);
  GPS.begin(9600);//Start connection to GPS
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY); //Set some setting for the GPS, need only basic data
  // Set the update rate
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_10HZ);   // 10 Hz update rate
  pinMode(inputpin, INPUT); // Set Pin 2 to input, to measure on circuit.
  GPS.sendCommand(PGCMD_ANTENNA);
  delay(1000); // Give some time to make sure we are ready. 

  Serial.println("Waiting for GPS fix");
}

void loop() {
  
  //unsigned long t1 = micros();
  
  char c = GPS.read(); //Allways read GPS module
  // if a sentence is received, we can check the checksum, parse it...
  if (GPS.newNMEAreceived()) {
    
    if (!GPS.parse(GPS.lastNMEA()))   // this also sets the newNMEAreceived() flag to false
      return;  // we can fail to parse a sentence in which case we should just wait for another
  }
  
  if (GPS.milliseconds==0){//We have reached a new second (so GPS.milliseconds will be 0)
    microTimer_offset=micros();//Time offset (micros overflows after approx. 1 hr)
    //At moment of overflow will cause some strange timing
  }
  
  //Code for checking if we should stop logging:
  if (Serial.available() > 0) {
    // read the incoming byte:
    message = Serial.read();
    if (message=='s'){ //corresponds to single 's' character, since we send as soon as we press button on computer in Putty
      Serial.println("Stopping logging session");
      printTime(GPS,microTimer_offset);
      Logging=false;
    }
  }
  
  if (Start){ // Wait in here until we get time-fix
    if ((int)GPS.fix==1){ //We have fix on GPS
      Serial.println("Starting Logging Session");
      printTime(GPS,microTimer_offset);
      Start=false;
      prevValue=digitalRead(inputpin);
    }
  } else { // We are actually logging
    
    //Code for logging:
    Readout = digitalRead(inputpin); // read pin value
    if (Readout!=prevValue and Logging){ //Compare to previous value
      Serial.println("\nChange!"); //Print message if we changed values
      prevValue=Readout; //set new prevValue
  
      printTime(GPS,microTimer_offset); //print current time
      
    } 
  }

  //unsigned long t2 = micros();
  //Serial.println(t2-t1);
}

void printTime(Adafruit_GPS GPS, unsigned long microTimer_offset){//Takes GPS as input along with internal timer and prints time to serial connection
  
  unsigned long microTimer=(micros()-microTimer_offset); //Compute microseconds since last second ticked over
  
  Serial.print("Time: "); //Note that this logs GMT
    if (GPS.hour < 10) { Serial.print('0'); }
    Serial.print(GPS.hour, DEC); Serial.print(':');
    if (GPS.minute < 10) { Serial.print('0'); }
    Serial.print(GPS.minute, DEC); Serial.print(':');
    if (GPS.seconds < 10) { Serial.print('0'); }
    Serial.print(GPS.seconds, DEC); Serial.print('.');
    int millisecond = microTimer/1000;
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
    Serial.println(microsecond);
    
    Serial.print("Date: ");
    Serial.print(GPS.day, DEC); Serial.print('/');
    Serial.print(GPS.month, DEC); Serial.print("/20");
    Serial.println(GPS.year, DEC);
}
