#include "display_manager.h"

DisplayManager::DisplayManager() : _display(CLK, DIO)
{
  this->reset();
}

// Reset the display
void DisplayManager::reset()
{
  _display.clear();
  _display.setBrightness(BRIGHTNESS);
}

// Display a number on the display
void DisplayManager::displayNumber(uint8_t number)
{
  uint8_t data[3] = {0, 0, 0};
  if (number >= 100)
  {
    // 3 digits number
    data[0] = _display.encodeDigit((number / 100) % 10);
    data[1] = _display.encodeDigit((number / 10) % 10);
  }
  else if (number >= 10)
  {
    // 2 digits number
    data[0] = _display.encodeDigit((number / 10) % 10);
  }
  // Last digit
  data[2] = _display.encodeDigit(number % 10);
  _display.setSegments(data, 3, 1);
}
