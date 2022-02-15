//Pining:
//Use digital 2 for signal

//variables
volatile unsigned long Count0=0;
volatile unsigned long Count1=0;
volatile unsigned long Count2=0;

void setup() {
  
  Serial.begin(19200); //This is what limits our detection freq: we send 280 bits each time, so 19200/280 = 68 Hz is actually our max rate we can log
  
  Serial.println("beginning");
  noInterrupts();
  PORTA.DIRCLR = PIN0_bm; 
  PORTA.PIN0CTRL = PORT_PULLUPEN_bm | PORT_ISC_FALLING_gc;
  
  PORTC.DIRCLR = PIN6_bm;
  PORTC.PIN6CTRL = PORT_PULLUPEN_bm | PORT_ISC_FALLING_gc;

  PORTF.DIRCLR = PIN5_bm; 
  PORTF.PIN5CTRL = PORT_PULLUPEN_bm | PORT_ISC_FALLING_gc;
  interrupts();

}

void loop() {
  Serial.println(Count0);
  Serial.println(Count1);
  Serial.println(Count2);
  delay(1000);
}



ISR(PORTC_PORT_vect){
  Count0=Count0+1;
  PORTC.INTFLAGS = 64;//clear Flag
}

ISR(PORTA_PORT_vect){
  Count1=Count1+1;
  PORTA.INTFLAGS = 1;//clear Flag
}

ISR(PORTF_PORT_vect){
  Count2=Count2+1;
  PORTF.INTFLAGS = 32;//clear Flag
}
