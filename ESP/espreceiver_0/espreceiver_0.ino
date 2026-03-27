#include <esp_now.h>
#include <WiFi.h>
#include <ArduinoJson.h>

// Struct of data
typedef struct struct_message {
  short id;
  float ax, ay, az;
  float gx, gy, gz;
  bool index, middle, ring, pinky;
} struct_message;

#define QUEUE_SIZE 10
QueueHandle_t dataQueue;

// Receive callback
void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  struct_message incoming;
  memcpy(&incoming, incomingData, sizeof(incoming));
  xQueueSendFromISR(dataQueue, &incoming, NULL);
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);

  // create queue
  dataQueue = xQueueCreate(QUEUE_SIZE, sizeof(struct_message));

  // Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // register for recv CB to get recv packer info
  esp_now_register_recv_cb(esp_now_recv_cb_t(OnDataRecv));
}

void loop() {
  struct_message receivedData;
  if (xQueueReceive(dataQueue, &receivedData, 0) == pdTRUE){
    //JSON code
    JsonDocument innoutBuffer;
    innoutBuffer["id"] = receivedData.id;

    innoutBuffer["ax"] = receivedData.ax;
    innoutBuffer["ay"] = receivedData.ay;
    innoutBuffer["az"] = receivedData.az;
    innoutBuffer["gx"] = receivedData.gx;
    innoutBuffer["gy"] = receivedData.gy;
    innoutBuffer["gz"] = receivedData.gz;

    innoutBuffer["index"] = receivedData.index ? 1 : 0;
    innoutBuffer["middle"] = receivedData.middle ? 1 : 0;
    innoutBuffer["ring"] = receivedData.ring ? 1 : 0;
    innoutBuffer["pinky"] = receivedData.pinky ? 1 : 0;

    String output;
    serializeJson(innoutBuffer, output);
    Serial.println(output);
}
  }
  






