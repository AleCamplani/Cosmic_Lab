volatile bool Start = false;
volatile bool Stop = false;
volatile unsigned long CounterAtStart=0;
volatile unsigned long CounterAtStop=0;

volatile unsigned long overflowCounter = 0;

unsigned long Difference=0;
unsigned long maxTimeDiff=10000; //in ns


void setup() {
  // set up clock counter:
  noInterrupts();
  //setup event-pin 1
  PORTF.DIRCLR = PIN5_bm; //pin PF5
  PORTF.PIN5CTRL = PORT_PULLUPEN_bm | PORT_ISC_RISING_gc;

  PORTMUX.TCBROUTEA = 2; //use alternative pin PF5 = D3

  //Connect the event-system:
  EVSYS.CHANNEL5 = 0x4D; //set channel 5 to use PF5 to get events
  EVSYS.USERTCB1 = 6; //user is TCB1, connect to channel 5=6-1

  //setup event-pin 2
  PORTA.DIRCLR = PIN2_bm; //pin PA2
  PORTA.PIN2CTRL = PORT_PULLUPEN_bm | PORT_ISC_RISING_gc;

  //PORTMUX.TCBROUTEA = PORTMUX.TCBROUTEA; //use normal pin PA2 = D20/SDA (and earlier setting)

  //Connect the event-system:
  EVSYS.CHANNEL0 = 0x42; //set channel 1 to use PA2 to get events
  EVSYS.USERTCB0 = 1; //user is TCB0, connect to channel 1=2-1

  //Set up clock for pin 1
  TCB1.CTRLB = 2; // Use COE mode
  TCB1.EVCTRL = 1; //enable input capture event
  TCB1.CCMP = 0; // set TOP (max is 2^16)
  TCB1.INTCTRL = 1; // Enable the interrupt on capture event
  TCB1.CTRLA = TCB_CLKSEL_CLKDIV1_gc | TCB_ENABLE_bm; // Use Timer as clock, enable timer

  //Set up clock for pin 2 - Has to be TCB0 to get right pin available
  TCB0.CTRLB = 2; // Use COE mode
  TCB0.EVCTRL = 1; //enable input capture event
  TCB1.CCMP = 0; // set TOP (max is 2^16)
  TCB0.INTCTRL = 1; // Enable the interrupt on capture event
  TCB0.CTRLA = TCB_CLKSEL_CLKDIV1_gc | TCB_ENABLE_bm; // Use Timer as clock, enable timer


  //Set up parralel timer
  TCB2.CTRLB = 0; // Use timer compare mode
  TCB2.EVCTRL = 0; //Periodic interrupt mode
  TCB2.CCMP = 65535; // set TOP (max is 2^16-1)
  TCB2.INTCTRL = 1; // Enable the interrupt
  TCB2.CTRLA = TCB_CLKSEL_CLKDIV1_gc | TCB_ENABLE_bm; // Use Timer as clock, enable timer
  
  
  interrupts();

  Serial.begin(19200);
}

void loop() {
  // put your main code here, to run repeatedly:
  if ((Start==true) and (Stop ==true)){ //We had event
    Difference=CounterAtStop-CounterAtStart;
    if (Difference*62.5<maxTimeDiff){ //only record if reasonable event
      Serial.println(Difference*62.5); //time difference in ns
      Serial.println(overflowCounter*62.5*TCB2.CCMP/1000000000);//time in s  
    }
    
    //lower flags:
    Stop=false;
    Start=false;
  }
  delay(10);
}


ISR(TCB1_INT_vect){ //call on Start
  CounterAtStart = TCB1.CCMP;
  Start=true;
  Stop=false;
  TCB1.INTFLAGS = TCB_CAPT_bm; //clear flag
}

ISR(TCB0_INT_vect){ //call on Stop
  CounterAtStop = TCB0.CCMP;
  if (Start==true){Stop=true;} //only raise flag if we have stop after start
  TCB0.INTFLAGS = TCB_CAPT_bm; //clear flag
}

ISR(TCB2_INT_vect){ //Call when we reach TOP
  //Keep others in sync
  TCB1.CNT=0;
  TCB0.CNT=0;
  
  //increment counter
  overflowCounter+=1;
  TCB2.INTFLAGS = TCB_CAPT_bm; //clear flag
}




ISR(PORTF_PORT_vect){ // called by pin event
  PORTF.INTFLAGS = 32;//clear Flag
}
ISR(PORTA_PORT_vect){ // called by pin event
  PORTA.INTFLAGS = 4;//clear Flag
}
