#include "display_manager.h"

DisplayManager displayManager;

void setup()
{
  Serial.begin(9600);
  Serial.println("Serial is setup");
}

void loop()
{
  displayManager.displayNumber(43);
  Serial.println("Display number 43");
  delay(1000);

  displayManager.reset();
  Serial.println("Display reset");
  delay(1000);
}
