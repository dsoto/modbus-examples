// This code is designed for an Arduino Mega
// Serial 1 TX to ASI TTL RX
// Serial 1 RX to ASI TTL TX
// Arduino GND to ASI GND

#include <ModbusMaster.h>

ModbusMaster node;         // create modbus master object
uint8_t result;            // modbus query result
int16_t response;          // modbus data response

uint16_t address = 265;    // address of battery voltage
float scale = 32.0;        // scale for battery voltage
uint8_t device_ID = 0x01;  // identifier for the ASI controller to distinguish from other devices

void setup() {

  Serial.begin(9600);               // Serial is the USB connector on the Arduino Mega
  Serial.println("ASI-MWE begin");

  Serial1.begin(115200);            // Serial1 is for the ASI controller
  node.begin(device_ID, Serial1);   // associate modbus node with device and serial port


}

void loop() {

  result = node.readHoldingRegisters(address, 1);  // query the ASI
  response = node.getResponseBuffer(0);            // get the result from ASI
  Serial.print("reading: ");
  Serial.println(response/scale);                  // write scaled reading to console

  delay(1000);

}
