volatile bool event = false;

void setup() {
  // set up clock counter:
  noInterrupts();
  //setup event-pin
  PORTF.DIRCLR = PIN5_bm; //pin PF5
  PORTF.PIN5CTRL = PORT_PULLUPEN_bm | PORT_ISC_FALLING_gc;

  PORTMUX.TCBROUTEA = 2; //use alternative pin PF3 = D3

  TCB1.CTRLB = 1; // Use TOCM mode
  TCB1.EVCTRL = 0; //disable input capture event
  TCB1.CCMP = 65000; // set TOP (max is 2^16)
  TCB1.INTCTRL = 1; // Enable the interrupt on capture
  TCB1.CTRLA = TCB_CLKSEL_CLKDIV1_gc | TCB_ENABLE_bm; // Use Timer as clock, enable timer
  interrupts();

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (event==true){
    Serial.println("Event!");
    event=false;
  }
  delay(100);
}

ISR(TCB1_INT_vect){ //Call when we reach TOP
  event=true;
  TCB1.INTFLAGS = TCB_CAPT_bm; //clear flag
}

ISR(PORTF_PORT_vect){ // called by pin event
  event=true;
  PORTF.INTFLAGS = 32;//clear Flag
}
