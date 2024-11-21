#!/bin/bash

echo "Installing dependencies..."
pip install .

if [ $? -eq 0 ]; then
  echo "Installation successful!"
else
  echo "Error: Installation failed!"
  exit 1
fi

echo "Generating config.json..."
python post_installation/create_config.py


if [ $? -eq 0 ]; then
  echo "Config.json generated successfully!"
else
  echo "Error: Failed to generate config.json!"
  exit 1
fi

echo "All done!"