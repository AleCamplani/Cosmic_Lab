/*
This script will use an Arduino UNO to generate pulses of a certain length.

Plan:
Use the timer1 object to run in a mode where when we reach a certain value, we switch the a pin from low to high and vice versa. 



 */

volatile bool State = false;


void setup() {
  
  Serial.begin(19200);

  //setup pin8 (PORTB0):
  DDRB = 1;


  //set timer0 interrupt at 2kHz
  TCCR0A = 0;// set entire TCCR2A register to 0
  TCCR0B = 0;// same for TCCR2B
  TCNT0  = 0;//initialize counter value to 0
  // set compare match register, each is 62.5ns, minimum is 40. 
  OCR0A = 40;
  // turn on CTC mode
  TCCR0A |= (1 << WGM01);
  // Set CS00 bit for no prescaler
  TCCR0B |= (1 << CS00);   
  // enable timer compare interrupt
  TIMSK0 |= (1 << OCIE0A);


  sei();
  
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(State);
}

ISR(TIMER0_COMPA_vect){ //Run the ISR
  if (State){PORTB=0;State=false;}
  else {PORTB=1;State=true;}
}
