// Garden Sensor module Nano + Rpi2
#include "Adafruit_AM2320.h"
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <Adafruit_BMP085.h>
#include <OneWire.h>
#include <DallasTemperature.h>

int mq4_pin = A1;
int mq7_pin = A0;
int soil_m_pin = A2;
int temp_probe_pin = 3;

int loops = 10;

float t_output = 0; // temp
float h_output = 0; // humid
float p_output = 0; // pressure
float m_output = 0; // moist
float mq4_output = 0;
float mq7_output = 0;

Adafruit_AM2320 am2320 = Adafruit_AM2320();
Adafruit_BMP085 bmp;
OneWire oneWire(temp_probe_pin);
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(9600);
  
  // AM2320
  am2320.begin();

  // MQ4
  pinMode(mq4_pin, INPUT);

  // MQ7
  pinMode(mq7_pin, INPUT);

  // BMP180
  if (!bmp.begin()) {
    Serial.println("Could not find a valid BMP085 sensor, check wiring!");
    while (1) {}
  }

  // temp probe
  sensors.begin();
}

void loop() {
  if (Serial.available() > 0) {
    int inByte = Serial.read();
    switch (inByte) {
        case '1':
          h_output = 0;
          for (int i = 0; i <= loops; i++) {
            float h_read = am2320.readHumidity();
            h_output = h_output + h_read;
            delay(10);
          }
          h_output = h_output/loops;
          Serial.println(h_output, 1);
          break;

        case '2':
          t_output = 0;
          for (int i = 0; i <= loops; i++) {
            float t_read = am2320.readTemperature();
            t_output = t_output + t_read;
            delay(10);
          }
          t_output = t_output/loops;
          Serial.println(t_output, 1);
          break;
        
        case '3':
          mq4_output = 0;
          for (int i = 0; i <= loops; i++) {
            float analogValue = analogRead(mq4_pin);
            mq4_output = mq4_output + analogValue;
            delay(10);
          }
          mq4_output = mq4_output/loops;
          Serial.println(map(mq4_output, 0, 1023, 0, 100), 1);
          break;
        
        case '4':
          mq7_output = 0;
          for (int i = 0; i <= loops; i++) {
            float analogValue = analogRead(mq7_pin);
            mq7_output = mq7_output + analogValue;
            delay(10);
          }
          mq7_output = mq7_output/loops;
          Serial.println(map(mq7_output, 0, 1023, 0, 100), 1);
          break;
        
        case '5':
          p_output = 0;
          for (int i = 0; i <= loops; i++) {
            float p_read = bmp.readPressure();
            p_output = p_output + p_read;
            delay(10);
          }
          p_output = p_output/loops;
          Serial.println(p_output, 1);
          break;

        case '6':
          t_output = 0;
          for (int i = 0; i <= loops; i++) {
            float t_read = bmp.readTemperature();
            t_output = t_output + t_read;
            delay(10);
          }
          t_output = t_output/loops;
          Serial.println(t_output, 1);
          break;
        
        case '7':
          t_output = 0;
          sensors.requestTemperatures(); 
          for (int i = 0; i <= loops; i++) {
            float t_read = sensors.getTempCByIndex(0);
            t_output = t_output + t_read;
            delay(10);
          }
          t_output = t_output/loops;
          Serial.println(t_output, 1);
          break;

        case '8':
          m_output = 0;
          for (int i = 0; i <= loops; i++) {
            float analogValue = analogRead(soil_m_pin);
            m_output = m_output + analogValue;
            delay(10);
          }
          m_output = m_output/loops;
          Serial.println(map(m_output, 0, 1023, 0, 100), 1);
          break;
      }
   }
}
