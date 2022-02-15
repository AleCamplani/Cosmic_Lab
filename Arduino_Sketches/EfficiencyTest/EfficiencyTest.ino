/*
 * Counts the number of events on different channels, and compares
 * 
 * 
 */

volatile long PulseA;
volatile long PulseB;

int Runtime = 3600; // in s

int StartTime=0;
int TimeNow=0;

int ElapsedTime=0;
int PrintedTime=0;

double A=0;
double B=0;
double Eff=0;

bool Running=true;

//Pinning:
// D2 is signal A
// D4 is signal B


void setup() {
  Serial.begin(38400);
  StartTime=millis()/1000;

  Serial.println("Starting");
  
  noInterrupts();
  PORTA.DIRCLR = PIN0_bm; 
  PORTA.PIN0CTRL = PORT_PULLUPEN_bm | PORT_ISC_FALLING_gc;
  
  PORTC.DIRCLR = PIN6_bm;
  PORTC.PIN6CTRL = PORT_PULLUPEN_bm | PORT_ISC_FALLING_gc;
  interrupts();

}

void loop() {
  if (Running){
    TimeNow=millis()/1000;
    ElapsedTime=TimeNow-StartTime;
    if (ElapsedTime>PrintedTime){
      Serial.print("Elapsed Time:");
      Serial.println(TimeNow-StartTime);
      Serial.println("Results Thus far:");
      Serial.println(PulseA);
      Serial.println(PulseB);
      A=PulseA;
      B=PulseB;
      Eff=B/(A+B);
      Serial.println(Eff);//print efficiency;
      PrintedTime=ElapsedTime+10;
    }
    if ((TimeNow-StartTime)>Runtime){
      Serial.println("Time is Up!");
      Serial.println("Final counts:");
      Serial.println(PulseA);
      Serial.println(PulseB);
      A=PulseA;
      B=PulseB;
      Eff=B/(A+B);
      Serial.println(Eff);//print efficiency;
      Running=false;
    }  
  }
}

ISR(PORTA_PORT_vect){
  PulseA=PulseA+1;
  PORTA.INTFLAGS = 1;//clear Flag
}

ISR(PORTC_PORT_vect){
  PulseB=PulseB+1;
  PORTC.INTFLAGS = 64;//clear Flag
}
