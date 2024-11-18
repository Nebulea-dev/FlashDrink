#include "display_manager.h"

DisplayManager displayManager;

#include <MFRC522v2.h>
#include <MFRC522DriverSPI.h>
//#include <MFRC522DriverI2C.h>
#include <MFRC522DriverPinSimple.h>
#include <MFRC522Debug.h>

MFRC522DriverPinSimple ss_pin(10); // Configurable, see typical pin layout above.

MFRC522DriverSPI driver{ss_pin}; // Create SPI driver.
//MFRC522DriverI2C driver{}; // Create I2C driver.
MFRC522 mfrc522{driver};  // Create MFRC522 instance.

void setup()
{
  Serial.begin(9600);
  mfrc522.PCD_Init();  // Init MFRC522 board.
  MFRC522Debug::PCD_DumpVersionToSerial(mfrc522, Serial);	// Show details of PCD - MFRC522 Card Reader details.
  Serial.println("Serial is setup");
}

void loop()
{
  displayManager.displayNumber(43);
  delay(100);

  displayManager.reset();
  delay(100);

  if(mfrc522.PICC_IsNewCardPresent()) 
  {
    Serial.println("Card found !");
    
	// Select one of the cards.
	if(!mfrc522.PICC_ReadCardSerial()) 
    {
		return;
	}
	// Dump debug info about the card; PICC_HaltA() is automatically called.
    MFRC522Debug::PICC_DumpToSerial(mfrc522, Serial, &(mfrc522.uid));
  }
}
