#include <WiFi.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <WiFiUdp.h>
#include <ArduinoJson.h>

//WIFI stuff
const char* ssid = "UCI-Guest";  //ex: Velocity Wi-Fi
const char* password = "";    //enter password, here's bad security practice aka my password :)

const char* udpAddress = "10.7.119.116";  // PC's IP  // TODO: ***CHANGE THIS**** is there an automated way
const int udpPort = 5005;                 // Port on PC 

// macAddress
String espmacAddress = "";
WiFiUDP udp;

// MPU code
Adafruit_MPU6050 mpu;

JsonDocument JSONbuffer;
JsonObject JSONencoder = JSONbuffer.to<JsonObject>();

void setup() {
  // Init Serial Monitor
  Serial.begin(115200);

  //Connect to WiFi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");


  Serial.println("scan start");

  // WiFi.scanNetworks will return the number of networks found
  int n = WiFi.scanNetworks();
  Serial.println("scan done");
  if (n == 0) {
      Serial.println("no networks found");
  } else {
    Serial.print(n);
    Serial.println(" networks found");
    for (int i = 0; i < n; ++i) {
      // Print SSID and RSSI for each network found
      Serial.print(i + 1);
      Serial.print(": ");
      Serial.print(WiFi.SSID(i));
      Serial.print(" (");
      Serial.print(WiFi.RSSI(i));
      Serial.print(")");
      Serial.println((WiFi.encryptionType(i) == WIFI_AUTH_OPEN)?" ":"*");
      delay(10);
    }
  }
  Serial.println("");

  // Wait a bit before scanning again
  delay(5000);




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
}
 
void loop() {
  // // Set values to send



  sensors_event_t a, g, t;
  mpu.getEvent(&a, &g, &t);
  if (espmacAddress == "28:05:A5:32:DE:D0"){
    JSONbuffer["id"] = 1;
  }else if (espmacAddress == "B0:CB:D8:E9:63:28"){
    JSONbuffer["id"] = 2;
  }else{
    JSONbuffer["id"] = 3;
  }
  JSONbuffer["ax"] = a.acceleration.x;
  JSONbuffer["ay"] = a.acceleration.y;
  JSONbuffer["az"] = a.acceleration.z;
  JSONbuffer["gx"] = g.gyro.x;
  JSONbuffer["gy"] = g.gyro.y;
  JSONbuffer["gz"] = g.gyro.z;

  udp.beginPacket(udpAddress, udpPort);
  serializeJson(JSONbuffer, udp);
  udp.endPacket();
  serializeJson(JSONbuffer, Serial);
  Serial.println("");
  

  delay(200);
}






