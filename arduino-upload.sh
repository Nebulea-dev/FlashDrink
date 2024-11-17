#!/bin/bash

# Config
SKETCH="FlashDrink.ino"
BOARD="arduino:avr:yunmini"

# Directories
BUILD_DIR="build/$BOARD"

# Port
PORT=$1
if [ -z $PORT ]; then
  echo "Port série non spécifié."
  exit 1
fi

# Téléversement du projet
arduino-cli upload -p $PORT --fqbn $BOARD $BUILD_DIR/$SKETCH
if [ $? -ne 0 ]; then
  echo "Erreur lors du téléversement."
  exit 1
fi

echo "Téléversement réussi."