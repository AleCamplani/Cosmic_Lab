unsigned long overflowCounter = 0;
unsigned long nanoseconds = 0;
unsigned long Readout = 10;

void setup() {
  // set up clock counter:
  noInterrupts();
  TCB1.CTRLB = 0; // Use timer compare mode
  TCB1.EVCTRL = 0; //Periodic interrupt mode
  TCB1.CCMP = 65000; // set TOP (max is 2^16)
  TCB1.INTCTRL = 1; // Enable the interrupt
  TCB1.CTRLA = TCB_CLKSEL_CLKDIV1_gc | TCB_ENABLE_bm; // Use Timer as clock, enable timer
  interrupts();

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(TCB1.CNT); //Print the register where we store timer value
  Serial.println(overflowCounter);
  Serial.println(Readout);
  //Set to how many overflows we have, mutilpied by how much time passes between overflows and add current counter
  nanoseconds=overflowCounter*(TCB1.CCMP*62.5) + TCB1.CNT*62.5;
  overflowCounter=0;
  Serial.print("Nanoseconds passed: ");
  Serial.println(nanoseconds);
  
  
  delay(1000); // So as to not spam the console.
  
}

ISR(TCB1_INT_vect){ //Call when we reach TOP
  Readout=TCB1.CNT; //To check we reset CNT, apparently the interrupt takes 20 cycles
  overflowCounter+=1;
  TCB1.INTFLAGS = TCB_CAPT_bm; //clear flag
}
