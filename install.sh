#!/bin/bash

# Navigate to the script's directory
cd "$(dirname "$0")"

# Idempotent Checks
if [ -d "$HOME/.openclaw/eeg-input" ]; then
  echo "EEG directories already set up. Skipping creation steps.\n"
else
  mkdir -p $HOME/.openclaw/{eeg-input,eeg-processed,eeg-output}
  chmod 700 $HOME/.openclaw/eeg-*
  echo "EEG directories created successfully."
fi

# Check if venv is set up
if [[ ! -d "venv" ]]; then
  echo "Error: Virtual environment not found."
  echo -e "\nTo set up manually, use the following commands:\n"
  echo "    python3 -m venv venv"
  echo "    source venv/bin/activate"
  echo "    pip install --upgrade zuna torch torchaudio mne pylsl psutil"
  echo "Once done, re-run this script to complete the installation."
  exit 1
else
  echo "Virtual environment found. Verifying version of braindecode and dependencies..."
  source venv/bin/activate
  if pip show braindecode &>/dev/null; then
    BRAIND_CODE_VER=$(pip show braindecode | grep Version | awk '{print $2}')
    echo "Braindecode version installed: $BRAIND_CODE_VER"

    echo -e "\n📦 All setup steps are complete! Here are some commands you can use:\n"
    echo "1. To activate the virtual environment: source venv/bin/activate"
    echo "2. To run your project: node index.js"
    echo "3. To check dependencies: pip list"
    deactivate
  else
    echo "Error: Braindecode is not installed in the virtual environment. Please run the following commands to complete setup:\n"
    echo "    source venv/bin/activate"
    echo "    pip install --upgrade zuna torch torchaudio mne pylsl psutil"
    echo "    pip install braindecode"
    echo "Once done, re-run this script to verify setup."
    deactivate
    exit 1
  fi
fi

# Create config.json for the skill if it doesn't already exist
CONFIG_FILE="config.json"
if [ ! -f "$CONFIG_FILE" ]; then
  cat <<EOL >> $CONFIG_FILE
{
  "brainInput": {
    "provider": "local-zuna",
    "modelPath": "\"$HOME/.cache/huggingface/hub/models--Zyphra--ZUNA\"",
    "eegDirs": {
      "input": "$HOME/.openclaw/eeg-input",
      "processed": "$HOME/.openclaw/eeg-processed",
      "output": "$HOME/.openclaw/eeg-output"
    }
  },
  "plugins": {
    "bci-core": {
      "enabled": true
    }
  }
}
EOL
  echo "Generated config.json for 'braindecode' skill at $(pwd)/$CONFIG_FILE"
else
  echo "Config file already exists. Skipping creation."
fi

# Append monitoring to HEARTBEAT.md
echo "- EEG Health: Check ZUNA inference latency and resource use every 60s." >> $HOME/.openclaw/workspace/HEARTBEAT.md

echo "braindecode skill installed successfully! 🧠🐕"