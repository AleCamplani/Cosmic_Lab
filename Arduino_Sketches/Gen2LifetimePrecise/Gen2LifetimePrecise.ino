//#include <Adafruit_GPS.h> // GPS Libraries
//#include <SoftwareSerial.h>

//SoftwareSerial mySerial(8, 9); //TX,RX
//Adafruit_GPS GPS(&mySerial);

//To track state:
bool startup=false; 
bool logging=true;
bool Ready=false;

//Pinning:
int SignalPin = 2; //signal from coincidence on two top, and anticoincidence on bottom
int DecayPin = 4; //signal from middle detector
int PPSPin = 3; //PPS pulse from GPS

//variables
volatile unsigned long second;
int minute;
int hour;

volatile unsigned long cyclesInSecond; //clockcycles we had last second

volatile unsigned long overflowCounter = 0; //Counts overflows in clock (every 4 ms this hapens)
volatile float clkSpeed=62.5;//clockspeed in ns, updated along the way

volatile bool EventFlag=false; //flag for recording events
volatile bool CandidateFlag=false; //flag for recording if we are listening for decay

volatile unsigned long EventNanosec; //record time of event
volatile unsigned long EventSec;
volatile unsigned long LifetimeNanosec; //record lifetime of muon.

void setup() {
  
  Serial.begin(19200); //This is what limits our detection freq: we send 280 bits each time, so 19200/280 = 68 Hz is actually our max rate we can log
  //GPS.begin(9600);//Start connection to GPS
  //GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY); //Tell GPS we only need basic data
  //GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate

  Serial.println("Waiting for GPS Fix");

  // set up main clock counter:
  noInterrupts();
  TCB1.CTRLB = 0; // Use timer compare mode
  TCB1.EVCTRL = 0; //Periodic interrupt mode
  TCB1.CCMP = 65000; // set TOP (max is 2^16)
  TCB1.INTCTRL = 1; // Enable the interrupt
  TCB1.CTRLA = TCB_CLKSEL_CLKDIV1_gc | TCB_ENABLE_bm; // Use Timer as clock, enable timer


  // set up secondary clock counter:
  TCB0.CTRLB = 0; // Use timer compare mode
  TCB0.EVCTRL = 0; //Periodic interrupt mode
  TCB0.CCMP = 6500; // set TOP (max is 2^16)
  TCB0.INTCTRL = 1; // Enable the interrupt
  TCB0.CTRLA = TCB_CLKSEL_CLKDIV1_gc; // Use Timer as clock , do not enable (yet)

  // Set up interrupts from pins:
  PORTA.DIRCLR = PIN0_bm; //Event pin
  PORTA.PIN0CTRL = PORT_PULLUPEN_bm | PORT_ISC_FALLING_gc;

  PORTC.DIRCLR = PIN6_bm; //Decay pin
  PORTC.PIN6CTRL = PORT_PULLUPEN_bm | PORT_ISC_FALLING_gc;

  PORTF.DIRCLR = PIN5_bm; //PPS pin
  PORTF.PIN5CTRL = PORT_PULLUPEN_bm | PORT_ISC_FALLING_gc;
  
  interrupts();
  
}

void loop() {
  //main loop
  if(startup) {
    //Startup();
  } else if (logging) {
    Normal();
  } else {
    //Do nothing
  }
  
}

//void Startup(){
  //Run this until we have time from GPS  
  
  //char c = GPS.read(); //read GPS module
  //if (GPS.newNMEAreceived()) {//If we received something, parse it
  //  if (!GPS.parse(GPS.lastNMEA()))   // this also sets the newNMEAreceived() flag to false
  //    return;  // we can fail to parse a sentence in which case we should just wait for another
  //}

  //if (((GPS.day != 0) and (Ready==false)) and (GPS.fix==true)){ //The GPS sent us a time, so get ready to start!
  //  minute=GPS.minute; //save time we got
  //  second=GPS.seconds;
  //  hour=GPS.hour;

  //  Serial.print("GPS Fix obtained at;");
  //  printTime(second,0,true);
    
  //  Ready=true; // Go into normal mode when next second ticks
  //}
  
//}

void Normal(){
  //Normal operating loop
  
  CheckPulse(); //Check if we need to print about an event
  
  StopLoggingCheck(); //Check if we should stop
}


void CheckPulse(){
  //Check if we had an event 
  if (EventFlag){
    Serial.print("Lifetime;");
    if (LifetimeNanosec<10){
      Serial.print("00000");}
    else if (LifetimeNanosec<100){
      Serial.print("0000");}
    else if (LifetimeNanosec<1000){
      Serial.print("000");}
    else if (LifetimeNanosec<10000){
      Serial.print("00");}
    else if (LifetimeNanosec<100000){
      Serial.print("0");}
    Serial.print(LifetimeNanosec);
    Serial.print(";");
    printTime(EventSec,EventNanosec,false);
    EventFlag=false; //lower flag
  }
}

ISR(PORTA_PORT_vect){
  //Interrupt ISR for the signals from the detectors
  //Will override waiting for decay, this is intentional
  if (EventFlag==false){ //only record of we have lowered flag from last event
    EventNanosec = NanosecondsNow(); //# of cylces times clockspeed (since second ticked over)
    EventSec=second;
    CandidateFlag=true; //raise flag for possible lifetime measurement
    //Enable secondary timer:
    TCB0.CNT = 0; //reset counter
    TCB0.CTRLA = TCB_CLKSEL_CLKDIV1_gc | TCB_ENABLE_bm;    
    
  }
  PORTA.INTFLAGS = 1;//clear Flag
}

ISR(PORTC_PORT_vect){
  //ISR for when something decays
  if (CandidateFlag==true){ //only do something if we are looking for decays, should be reduntant check
    LifetimeNanosec = clkSpeed*TCB0.CNT; //time since candiadateflag was set. 
    CandidateFlag=false; //reset flag
    EventFlag=true; //we have something we want to record  
  }
  PORTC.INTFLAGS = 64;//clear Flag
}

unsigned long NanosecondsNow(){
  return (overflowCounter * TCB1.CCMP + TCB1.CNT)*clkSpeed;
}


ISR(PORTF_PORT_vect){
  //called every sec by GPS
  cyclesInSecond = overflowCounter * TCB1.CCMP + TCB1.CNT; //How many cycles passed since last PPS event
  clkSpeed=1e9/cyclesInSecond; //Recompute clockspeed (in ns)
  TCB1.CNT=0; //reset counter
  overflowCounter=0; //reset overflow, we entered new second
  second =  second + 1; //One second passed
  if (Ready==true and startup==true){
    startup=false; // we can enter normal mode
    EventFlag=false; // Disregard earlier events
  }
  PORTF.INTFLAGS = 32;//clear Flag
}

ISR(TCB1_INT_vect){ //Call when we reach TOP
  overflowCounter+=1; //We overflowed
  TCB1.INTFLAGS = TCB_CAPT_bm; //clear flag
}

ISR(TCB0_INT_vect){ //Call when we reach TOP on second
  TCB0.CTRLA = 0; //Disable timer
  TCB0.INTFLAGS = TCB_CAPT_bm; //clear flag
  CandidateFlag = false; //nothing decayed in timeframe
  //detachInterrupt(digitalPinToInterrupt(DecayPin)); //stop interrupt from middle
}

void StopLoggingCheck(){
  //This we call to check if we were told to stop
  if (Serial.available() > 0) {
    // read the incoming byte:
    char message = Serial.read();
    if (message=='s'){
      Serial.print("Stopping logging session;");
      printTime(second,NanosecondsNow(),true);
      logging=false;
    }
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
    //Serial.print(GPS.day, DEC); Serial.print('/');
    //Serial.print(GPS.month, DEC); Serial.print("/20");
    //Serial.println(GPS.year, DEC);
  } else {
    Serial.println(";");
  }
}
