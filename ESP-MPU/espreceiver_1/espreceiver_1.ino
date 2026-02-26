#include <esp_now.h>
#include <WiFi.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

// REPLACE WITH YOUR RECEIVER MAC Address
uint8_t broadcastAddress1[] = {0x28, 0x05, 0xa5, 0x32, 0xde, 0xd0}; //1st esp is receiver
                                                                   //0xb0, 0xcb, 0xd8, 0xe9, 0x63, 0x28

// Struct to send data
// Must match the receiver structure
typedef struct struct_message {
  sensors_event_t a, g, temp;
} struct_message;

// Create a struct_message called myData
struct_message myData;

//HEREesp_now_peer_info_t peerInfo;

// callback when data is sent
//HEREvoid OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
//HERE  Serial.print("\r\nLast Packet Send Status:\t");
//HERE  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
//HERE}

// callback function that will be executed when data is received
void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  memcpy(&myData, incomingData, sizeof(myData));
  //ACCELERATION                                    Acceleration X: 3.33, Y: 5.55, Z: 7.77 m/s^2
  Serial.print("Acceleration2 X:");
  Serial.print(myData.a.acceleration.x);
  Serial.print(", Y: ");
  Serial.print(myData.a.acceleration.y);
  Serial.print(", Z: ");
  Serial.print(myData.a.acceleration.z);
  Serial.println(" m/s^2");

  //ROTATION                                        Rotation X: 1.01, Y: 2.02, Z: -4.05 rad/s
  Serial.print("Rotation2 X: ");
  Serial.print(myData.g.gyro.x);
  Serial.print(", Y: ");
  Serial.print(myData.g.gyro.y);
  Serial.print(", Z: ");
  Serial.print(myData.g.gyro.z);
  Serial.println(" rad/s");

  Serial.println();
}

// MPU code
Adafruit_MPU6050 mpu;

void setup() {
  // Init Serial Monitor
  Serial.begin(115200);
 
  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  // Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // // Once ESPNow is successfully Init, we will register for Send CB to
  // // get the status of Trasnmitted packet
  // esp_now_register_send_cb(esp_now_send_cb_t(OnDataSent));
  esp_now_register_recv_cb(esp_now_recv_cb_t(OnDataRecv));
  
  // // Register peer
  // memcpy(peerInfo.peer_addr, broadcastAddress1, 6);
  // peerInfo.channel = 0;  
  // peerInfo.encrypt = false;
  
  // // Add peer        
  // if (esp_now_add_peer(&peerInfo) != ESP_OK){
  //   Serial.println("Failed to add peer");
  //   return;
  // }

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

  Serial.print("Acceleration1 X:");
  Serial.print(a.acceleration.x);
  Serial.print(", Y: ");
  Serial.print(a.acceleration.y);
  Serial.print(", Z: ");
  Serial.print(a.acceleration.z);
  Serial.println(" m/s^2");

  //ROTATION
  Serial.print("Rotation1 X: ");
  Serial.print(g.gyro.x);
  Serial.print(", Y: ");
  Serial.print(g.gyro.y);
  Serial.print(", Z: ");
  Serial.print(g.gyro.z);
  Serial.println(" rad/s");
  Serial.println();

  // // Send message via ESP-NOW
  // esp_err_t result = esp_now_send(broadcastAddress1, (uint8_t *) &myData, sizeof(myData));
   
  // if (result == ESP_OK) {
  //   Serial.println("Sent with success");
  //   Serial.println();
  // }
  // else {
  //   Serial.println("Error sending the data");
  // }
  delay(200);
}
