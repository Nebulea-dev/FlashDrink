#ifndef DISPLAY_MANAGER_H
#define DISPLAY_MANAGER_H

#include <Arduino.h>
#include <TM1637Display.h>

// Module connection pins (Digital Pins)
#define CLK 2
#define DIO 3

class DisplayManager
{
private:
  static const uint8_t BRIGHTNESS = 0x0f;
  TM1637Display _display;

public:
  DisplayManager();
  void reset();
  void displayNumber(uint8_t number);
};

#endif // DISPLAY_MANAGER_H
