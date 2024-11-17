#include "display_manager.h"

DisplayManager displayManager;

void setup()
{
  // Nothing to do here
}

void loop()
{
  displayManager.displayNumber(42);
  delay(1000);
  displayManager.reset();
  delay(1000);
}