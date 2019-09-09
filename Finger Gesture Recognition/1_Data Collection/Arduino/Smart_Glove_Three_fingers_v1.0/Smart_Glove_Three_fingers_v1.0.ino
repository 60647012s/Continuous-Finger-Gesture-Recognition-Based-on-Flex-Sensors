#include "Wire.h"  // 引入 Serial, pinMode 等等
#include <SoftwareSerial.h>  // 引入 Bluetooth 相關函式。如：SoftwareSerial bluetooth()
#include <Timer.h>  // 引入 trigger 函式

#define BT_TX_PIN 6  // 宣告 Bluetooth TX Pin
#define BT_RX_PIN 8  // 宣告 Bluetooth RX Pin
SoftwareSerial bluetooth(BT_TX_PIN, BT_RX_PIN);  // 建立 RX 與 TX 的傳輸
Timer trigger;  // 功能：每隔故定 Xms 執行一次 "某個函式"。

const int FLEX_PIN_1 = A4;    // Flex0 Sensor Pin - Thumb
const int FLEX_PIN_2 = A2;    // Flex1 Sensor Pin - Index
const int FLEX_PIN_3 = A0;    // Flex2 Sensor Pin - Midium

int Get_Flex_Data(int);    // Retrun int = Analogy Volt., Input int = Flex Sensor's ADCPin
void Bluetooth_Transfer();  // Bluetooth Transfer    

// Segmentation flex data to 1 + 1 byte from 2byte. Because bluetooth transmission just have 1 byte
union F_DataSplit  // Flex Sensor_Data Split
{
    unsigned char split[2];
    int full;
}F_Data1, F_Data2, F_Data3;

void setup() 
{
  bluetooth.begin(9600);
  delay(300);
  Serial.begin(115200);
  delay(300);
  pinMode(FLEX_PIN_1, INPUT);    // Declare flex0 pin
  pinMode(FLEX_PIN_2, INPUT);    // Declare flex1 pin
  pinMode(FLEX_PIN_3, INPUT);    // Declare flex2 pin
  trigger.every(20, Bluetooth_Transfer);  // 每 20ms 觸發一次 Bluetooth_Transfer()
}

void loop() 
{
  F_Data1.full = Get_Flex_Data(FLEX_PIN_1);
  F_Data2.full = Get_Flex_Data(FLEX_PIN_2);
  F_Data3.full = Get_Flex_Data(FLEX_PIN_3);
  
  trigger.update();
}

// Return F_ADC_Vlot = Flex Sensor's ADC PIN's Vlot.
int Get_Flex_Data(int FLEX_PIN)
{
  int F_ADC_Vlot = analogRead(FLEX_PIN);  // F_ADC_Vlot = Flex Sensor's ADC PIN's Vlot.
  return F_ADC_Vlot;
}

// Bluetooth_Transfer
void Bluetooth_Transfer()
{
  bluetooth.write('S');
  bluetooth.write(F_Data1.split[0]);
  bluetooth.write(F_Data1.split[1]);
  bluetooth.write(F_Data2.split[0]);
  bluetooth.write(F_Data2.split[1]);
  bluetooth.write(F_Data3.split[0]);
  bluetooth.write(F_Data3.split[1]);
}
