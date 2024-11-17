#!/bin/bash

# Config
SKETCH="FlashDrink.ino"
BOARD="arduino:avr:yunmini"

# Directories
BUILD_DIR="build/$BOARD"
LIBRARIES_DIR="lib"
INCLUDE_DIR="include"

# Clean the build directory
rm -rf $BUILD_DIR
mkdir -p $BUILD_DIR

# Compilation
arduino-cli compile --fqbn $BOARD --build-path $BUILD_DIR --libraries $LIBRARIES_DIR --build-property "compiler.cpp.extra_flags=-I$INCLUDE_DIR" $SKETCH
if [ $? -ne 0 ]; then
  echo "Erreur lors de la compilation."
  exit 1
fi

echo "Compilation réussie."
