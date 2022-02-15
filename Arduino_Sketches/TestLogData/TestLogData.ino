#include <timestamp32bits.h> // timestamping library

timestamp32bits stamp = timestamp32bits(); //create instance of timestamp object

int Readout=0; // To store readout value
int inputpin = 2; // Pin we read from

int prevValue=0; // Vaæue we compare to, to check for change

//Input starting time:

int Start_year = 2021-1970;
int Start_month = 10;
int Start_day = 18;
int Start_hours = 14;
int Start_minutes = 10;
int Start_sec = 0;

int now; //used for timekeeping
int year;
int month;
int day;
int hours;
int minutes;
int sec;

bool Logging = true; //To keep track of logging
String message;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); // Start serial connection for logging
  Serial.println("Starting");
  pinMode(inputpin, INPUT); // Set Pin A0 to input, to measure on circuit.

  
}

void loop() {
  //millis will overflow after approx. 50 days. So fine to use for this litte test
  //Code for timekeeping:
  now=millis();
  sec=(Start_sec+now/1000)%60;
  minutes=(Start_minutes+(Start_sec+now/1000)/60)%60;
  hours=(Start_hours+(Start_minutes+(Start_sec+now/1000)/60)/60)%24;
  day=Start_day; //Assume that we run experiment on much smaller timescale than one day, so we do not bother keeping track
  month=Start_month;
  year=Start_year;

  //Code for checcking if we should stop logging:
  
  if (Serial.available() > 0) {
      // read the incoming byte:
      message = Serial.read();
  
      if (message=="115"){ //corresponds to single 's' character, since we send as soon as we press button on computer in Putty
        Serial.println("Stopping logging session");
        Serial.end();
        Logging=false;
      }
  }
  
  
  
  //Code for logging:
  Readout = digitalRead(inputpin); // read pin value
  if (Readout!=prevValue and Logging){ //Compare to previous value
    Serial.println("Change!"); //Print message if we changed values
    prevValue=Readout; //set ned prevValue
    Serial.println(String(hours)+":"+String(minutes)+":"+String(sec)); //Print time
    Serial.println(stamp.timestamp(year,month,day,hours,minutes,sec)); //Print timestamp
  }
  
}
