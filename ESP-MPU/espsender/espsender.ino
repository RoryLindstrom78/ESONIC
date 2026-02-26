#include <WiFi.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <WiFiUdp.h>

//WIFI stuff
const char* ssid = "";        //ex: Velocity WiFi
const char* password = "";    // enter password

const char* udpAddress = "";  // PC's IP
const int udpPort = 61000;    // Port on PC

WiFiUDP udp;

// MPU code
Adafruit_MPU6050 mpu;

void setup() {
  // Init Serial Monitor
  Serial.begin(115200);

  //Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Connected. IP: ");
  Serial.println(WiFi.localIP());
  
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
}
 
void loop() {
  // // Set values to send
  sensors_event_t a, g, t;
  mpu.getEvent(&a, &g, &t);

  String dataString = "";
  dataString += "Accel2 X:" + String(a.acceleration.x) + ", Y:" + String(a.acceleration.y) + ", Z:" + String(a.acceleration.z);
  dataString += " | Gyro2 X:" + String(g.gyro.x) + ", Y:" + String(g.gyro.y) + ", Z:" + String(g.gyro.z);

  udp.beginPacket(udpAddress, udpPort);
  udp.print(dataString);
  udp.endPacket();

  Serial.println(dataString);  
  delay(200);
}






