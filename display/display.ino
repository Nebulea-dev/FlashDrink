#include <Arduino.h>
#include <TM1637Display.h>

// Module connection pins (Digital Pins)
#define CLK 2
#define DIO 3

TM1637Display display(CLK, DIO);

uint8_t data[] = {display.encodeDigit(0), display.encodeDigit(0), display.encodeDigit(0), display.encodeDigit(0)};

void setup() {
  display.setBrightness(0x0f);
}

void loop()
{
  display.setSegments(data);
  // Attend 1 seconde.
  delay (1000);
}