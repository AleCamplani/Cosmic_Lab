volatile bool event = false;
volatile bool event1 = false;
volatile unsigned long CounterAtEvent=0;
volatile unsigned long CounterNow=0;
volatile unsigned long parallelCounter=0;

volatile unsigned long overflowCounter = 0;

void setup() {
  // set up clock counter:
  noInterrupts();
  //setup event-pin
  PORTF.DIRCLR = PIN5_bm; //pin PF5
  PORTF.PIN5CTRL = PORT_PULLUPEN_bm | PORT_ISC_BOTHEDGES_gc;

  PORTMUX.TCBROUTEA = 2; //use alternative pin PF5 = D3

  //Connect the event-system:
  EVSYS.CHANNEL5 = 0x4D; //set channel 5 to use PF5 to get events
  EVSYS.USERTCB1 = 6; //user is TCB1, connect to channel 5=6-1
  
  TCB1.CTRLB = 2; // Use COE mode
  TCB1.EVCTRL = 1; //enable input capture event
  TCB1.CCMP = 65000; // set TOP (max is 2^16)
  TCB1.INTCTRL = 1; // Enable the interrupt on capture event
  TCB1.CTRLA = TCB_CLKSEL_CLKDIV1_gc | TCB_ENABLE_bm; // Use Timer as clock, enable timer


  //Set up parralel timer
  TCB0.CTRLB = 0; // Use timer compare mode
  TCB0.EVCTRL = 0; //Periodic interrupt mode
  TCB0.CCMP = 65000; // set TOP (max is 2^16)
  TCB0.INTCTRL = 1; // Enable the interrupt
  TCB0.CTRLA = TCB_CLKSEL_CLKDIV1_gc | TCB_ENABLE_bm; // Use Timer as clock, enable timer
  
  
  interrupts();

  Serial.begin(19200);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (event==true){
    Serial.println("Event!");
    Serial.println(overflowCounter);
    Serial.println((CounterNow-CounterAtEvent)*62.5); //gives random values, there is hope yet!
    Serial.println(CounterAtEvent);
    Serial.println(parallelCounter);
    Serial.println(CounterNow);
    if (parallelCounter>=CounterNow){ //seems this difference is not constant...
      Serial.println(parallelCounter-CounterNow);   
    } else {
      Serial.println(CounterNow-parallelCounter); 
    }
    
    event=false;
  }
  if (event1==true){
    //Serial.println("Pin");
    event1=false;
  }
  delay(100);
}

ISR(TCB1_INT_vect){ //call on event
  CounterAtEvent=TCB1.CCMP;
  parallelCounter=TCB0.CNT;
  CounterNow=TCB1.CNT;
  event=true;
  TCB1.INTFLAGS = TCB_CAPT_bm; //clear flag
}

ISR(TCB0_INT_vect){ //Call when we reach TOP
  TCB1.CNT=0;//Keep other in sync
  overflowCounter+=1;
  TCB0.INTFLAGS = TCB_CAPT_bm; //clear flag
}

ISR(PORTF_PORT_vect){ // called by pin event //NEED THIS to lower flag
  event1=true;
  PORTF.INTFLAGS = 32;//clear Flag
}
