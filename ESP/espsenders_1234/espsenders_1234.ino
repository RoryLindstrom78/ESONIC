#include <esp_now.h>
#include <WiFi.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

// REPLACE WITH YOUR RECEIVER MAC Address
// uint8_t broadcastAddress1[] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00}; //0th esp is receiver
                                                                   //0xb0, 0xcb, 0xd8, 0xe9, 0x63, 0x28
uint8_t broadcastAddress1[] = {0x70, 0x4b, 0xca, 0x25, 0xc1, 0xe8}; //TODO: CHANGE THIS TO ONE

// Struct to send data
typedef struct struct_message {
  short id;
  float ax, ay, az;
  float gx, gy, gz;
  bool index, middle, ring, pinky;
} struct_message;

struct_message sentData;
esp_now_peer_info_t peerInfo;

bool sendSuccess = false;
// Send callback
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  sendSuccess = (status == ESP_NOW_SEND_SUCCESS);
}

//macAddress
String espmacAddress = "";

// MPU code
Adafruit_MPU6050 mpu;

// Button code
const int index_buttonPIN = 19;
const int middle_buttonPIN = 18;
const int ring_buttonPIN =5;
const int pinky_buttonPIN = 17;

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
bool index(){
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
bool middle(){
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
bool ring(){
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
bool pinky(){
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
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);

  // Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Once ESPNow is successfully Init, we will register for send CB to
  // get the status of Trasnmitted packet
  esp_now_register_send_cb(esp_now_send_cb_t(OnDataSent));
  
  // Register peer
  memcpy(peerInfo.peer_addr, broadcastAddress1, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  
  // Add peer        
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Failed to add peer");
    return;
  }

  // Getting the ESP mac address
  delay(100);
  espmacAddress = WiFi.macAddress();
  Serial.print("macAddress: ");
  Serial.println(espmacAddress);

  //MPU setup
  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");

  Serial.println("");
  delay(100);

  //button setup
  pinMode(index_buttonPIN, INPUT_PULLDOWN);
  pinMode(middle_buttonPIN, INPUT_PULLDOWN);
  pinMode(ring_buttonPIN, INPUT_PULLDOWN);
  pinMode(pinky_buttonPIN, INPUT_PULLDOWN);
}
 
void loop() {
  // Set values to send
  if (espmacAddress == "28:05:A5:32:DE:D0"){
    sentData.id = 1;
  }else if (espmacAddress == "B0:CB:D8:E9:63:28"){
    sentData.id = 2;
  }else if (espmacAddress == "70:4B:CA:26:43:E8"){
    sentData.id = 3;
  }else if (espmacAddress == "70:4B:CA:25:C1:E8"){
    sentData.id = 4;
  }else{
    sentData.id = 5;
  }

  sensors_event_t a, g, t;
  mpu.getEvent(&a, &g, &t);

  sentData.ax = a.acceleration.x;
  sentData.ay = a.acceleration.y;
  sentData.az = a.acceleration.z;

  sentData.gx = g.gyro.x;
  sentData.gy = g.gyro.y;
  sentData.gz = g.gyro.z;

  sentData.index = index();
  sentData.middle = middle();
  sentData.ring = ring();
  sentData.pinky = pinky();

  // Send message via ESP-NOW
  esp_err_t result = esp_now_send(broadcastAddress1, (uint8_t *) &sentData, sizeof(sentData));
   
   //printing to serial monitor
  if (result == ESP_OK) {
    Serial.print("\r\nLast Packet Send Status:\t");
    Serial.println(sendSuccess ? "Delivery Success" : "Delivery Fail");
    
    //ID
    Serial.print("ID:");
    Serial.println(sentData.id);

    //ROTATION
    Serial.print("Acceleration X:");
    Serial.print(sentData.ax);
    Serial.print(", Y: ");
    Serial.print(sentData.ay);
    Serial.print(", Z: ");
    Serial.print(sentData.az);
    Serial.println(" m/s^2");

    Serial.print("Rotation X: ");
    Serial.print(sentData.gx);
    Serial.print(", Y: ");
    Serial.print(sentData.gy);
    Serial.print(", Z: ");
    Serial.print(sentData.gz);
    Serial.println(" rad/s");

    //BUTTON
    Serial.print("Index: ");
    Serial.print(sentData.index);
    Serial.print(", Middle: ");
    Serial.print(sentData.middle);
    Serial.print(", Ring: ");
    Serial.print(sentData.ring);
    Serial.print(", Pinky: ");
    Serial.print(sentData.pinky);
    Serial.println();
  }
  else {
    Serial.println("Error sending the data");
  }
  delay(200);
}
