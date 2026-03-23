#include <WiFi.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <WiFiUdp.h>
#include <ArduinoJson.h>

//WIFI stuff
const char* ssid = "";  //ex: Velocity Wi-Fi
const char* password = "";    //enter password, here's bad security practice aka my password :)

const char* udpAddress = "192.168.0.162";  // PC's IP  // TODO: ***CHANGE THIS**** is there an automated way
const int udpPort = 5005;                  // Port on PC

// macAddress
String espmacAddress = "";
WiFiUDP udp;

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

//JSON code
JsonDocument JSONbuffer;
JsonObject JSONencoder = JSONbuffer.to<JsonObject>();

void setup() {
  // Init Serial Monitor
  Serial.begin(115200);

  //Connect to WiFi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");

  // Serial.println("scan start");

  // // WiFi.scanNetworks will return the number of networks found
  // int n = WiFi.scanNetworks();
  // Serial.println("scan done");
  // if (n == 0) {
  //     Serial.println("no networks found");
  // } else {
  //   Serial.print(n);
  //   Serial.println(" networks found");
  //   for (int i = 0; i < n; ++i) {
  //     // Print SSID and RSSI for each network found
  //     Serial.print(i + 1);
  //     Serial.print(": ");
  //     Serial.print(WiFi.SSID(i));
  //     Serial.print(" (");
  //     Serial.print(WiFi.RSSI(i));
  //     Serial.print(")");
  //     Serial.println((WiFi.encryptionType(i) == WIFI_AUTH_OPEN)?" ":"*");
  //     delay(10);
  //   }
  // }
  // Serial.println("");

  // // Wait a bit before scanning again
  // delay(5000);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    Serial.print(WiFi.status());
  }
  Serial.println();
  Serial.print("Connected. Destination IP: ");
  Serial.println(udpAddress);

  // Getting the ESP mac address
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
  //udp.begin(udpPort);

  //button setup
  pinMode(index_buttonPIN, INPUT_PULLDOWN);
  pinMode(middle_buttonPIN, INPUT_PULLDOWN);
  pinMode(ring_buttonPIN, INPUT_PULLDOWN);
  pinMode(pinky_buttonPIN, INPUT_PULLDOWN);
}


 
void loop() {
  // // Set values to send
  if (espmacAddress == "28:05:A5:32:DE:D0"){
    JSONbuffer["id"] = 1;
  }else if (espmacAddress == "B0:CB:D8:E9:63:28"){
    JSONbuffer["id"] = 2;
  }else if (espmacAddress == "70:4B:CA:26:43:E8"){
    JSONbuffer["id"] = 3;
  }else if (espmacAddress == "70:4B:CA:25:C1:E8"){
    JSONbuffer["id"] = 4;
  }else{
    JSONbuffer["id"] = 5;
  }

  //MPU 
  sensors_event_t a, g, t;
  mpu.getEvent(&a, &g, &t);
  JSONbuffer["ax"] = a.acceleration.x;
  JSONbuffer["ay"] = a.acceleration.y;
  JSONbuffer["az"] = a.acceleration.z;
  JSONbuffer["gx"] = g.gyro.x;
  JSONbuffer["gy"] = g.gyro.y;
  JSONbuffer["gz"] = g.gyro.z;

  JSONbuffer["index"] = index(index_buttonPIN) ? 1 : 0;
  JSONbuffer["middle"] = middle(middle_buttonPIN) ? 1 : 0;
  JSONbuffer["ring"] = ring(ring_buttonPIN) ? 1 : 0;
  JSONbuffer["pinky"] = pinky(pinky_buttonPIN) ? 1 : 0;


  udp.beginPacket(udpAddress, udpPort);
  serializeJson(JSONbuffer, udp);
  udp.endPacket();
  serializeJson(JSONbuffer, Serial);
  Serial.println("");
  

  delay(200);
}






