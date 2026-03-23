//Button code

//Pins
const int index_buttonPIN = 19;
const int middle_buttonPIN = 18;
const int ring_buttonPIN =5;
const int pinky_buttonPIN = 17;

//State parameters for all fingers
int index_buttonState = 0;
int index_lastState = LOW;
int index_pushed = LOW;

int middle_buttonState = 0;
int middle_lastState = LOW;
int middle_pushed = LOW;

int ring_buttonState = 0;
int ring_lastState = LOW;
int ring_pushed = LOW;

int pinky_buttonState = 0;
int pinky_lastState = LOW;
int pinky_pushed = LOW;

//Index finger
bool index(int indexPIN){
  index_buttonState = digitalRead(index_buttonPIN);
  if(index_buttonState == HIGH){
    Serial.println("Index Button Pressed!");
    index_pushed = !index_pushed;
    delay(50);
  }
  //0 to 1 state
  if(index_pushed == HIGH && index_lastState == LOW){
    index_lastState = HIGH; //set last state to HIGH
    delay(50); //delay
  } //1 to 0 state
  else if(index_buttonState == HIGH && index_lastState == HIGH){
    index_lastState = LOW; //set last state to LOW
    delay(50);
  }
  return index_lastState;
}

//Middle finger
bool middle(int middlePIN){
  middle_buttonState = digitalRead(middle_buttonPIN);
  if(middle_buttonState == HIGH){
    Serial.println("Middle Button Pressed!");
    middle_pushed = !middle_pushed;
    delay(50);
  }
  //0 to 1 state
  if(middle_pushed == HIGH && middle_lastState == LOW){
    middle_lastState = HIGH; //set last state to HIGH
    delay(50); //delay
  }//1 to 0 state
  else if(middle_buttonState == HIGH && middle_lastState == HIGH){
    middle_lastState = LOW; //set last state to LOW
    delay(50);
  }
  return middle_lastState;
}

//Ring finger
bool ring(int ringPIN){
  ring_buttonState = digitalRead(ring_buttonPIN);
  if(ring_buttonState == HIGH){
    Serial.println("Ring Button Pressed!");
    ring_pushed = !ring_pushed;
    delay(50);
  }
  //0 to 1 state
  if(ring_pushed == HIGH && ring_lastState == LOW){
    ring_lastState = HIGH; //set last state to HIGH
    delay(50); //delay
  }//1 to 0 state
  else if(ring_buttonState == HIGH && ring_lastState == HIGH){
    ring_lastState = LOW; //set last state to LOW
    delay(50);
  }
  return ring_lastState;
}

//Pinky finger
bool pinky(int pinkyPIN){
  pinky_buttonState = digitalRead(pinky_buttonPIN);
  if(pinky_buttonState == HIGH){
    Serial.println("Left Pinky Button Pressed!");
    pinky_pushed = !pinky_pushed;
    delay(50);
  }
  //0 to 1 state
  if(pinky_pushed == HIGH && pinky_lastState == LOW){
    pinky_lastState = HIGH; //set last state to HIGH
    delay(50); //delay
  }//1 to 0 state
  else if(pinky_buttonState == HIGH && pinky_lastState == HIGH){
    pinky_lastState = LOW; //set last state to LOW
    delay(50);
  }
  return pinky_lastState;
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  //Initialize Left Hand Pinmodes:
  pinMode(index_buttonPIN, INPUT_PULLDOWN);
  pinMode(middle_buttonPIN, INPUT_PULLDOWN);
  pinMode(ring_buttonPIN, INPUT_PULLDOWN);
  pinMode(pinky_buttonPIN, INPUT_PULLDOWN);
}

void loop() {
  // call button functions for each button
  Serial.print("Index State: ");
  Serial.println(index(index_buttonPIN));

  Serial.print("Middle State: ");
  Serial.println(middle(middle_buttonPIN));

  Serial.print("Ring State: ");
  Serial.println(ring(ring_buttonPIN));

  Serial.print("Pinky State: ");
  Serial.println(pinky(pinky_buttonPIN));
  Serial.println("");
  
  delay(200);  
}