const fs = require('fs');
const { spawn } = require('child_process');
const path = require('path');

const EEG_INPUT = path.join(process.env.HOME, ".openclaw/eeg-input");
const EEG_PROCESSED = path.join(process.env.HOME, ".openclaw/eeg-processed");
const EEG_OUTPUT = path.join(process.env.HOME, ".openclaw/eeg-output");
const MEMORY_DB = path.join(process.env.HOME, ".openclaw/memory/main.sqlite");

// File watcher for real-time EEG file processing
fs.watch(EEG_INPUT, (eventType, filename) => {
  if (eventType === 'change' && filename.endsWith('.fif')) {
    console.log(`New EEG file detected: ${filename}. Starting decode process...`);
    decodeEEG(filename);
  }
});

function decodeEEG(filename) {
  const inputFile = path.join(EEG_INPUT, filename);

  const pyProc = spawn('bash', ['-c', `source ${path.join(__dirname, 'venv/bin/activate')} && python3 decode_eeg.py ${inputFile} ${EEG_PROCESSED} ${EEG_OUTPUT}`]);

  pyProc.stdout.on('data', (data) => {
    console.log("[Python Output]: " + data.toString());
  });

  pyProc.stderr.on('data', (data) => {
    console.error("[Python Error]: " + data.toString());
  });

  pyProc.on('close', (code) => {
    if (code === 0) {
      console.log("EEG data from " + filename + " decoded successfully.");
      indexToMemory();
    } else {
      console.error("Python process exited with code " + code + ".");
    }
  });
}

// Index decoded thoughts into OpenClaw Memory and vector DB
function indexToMemory() {
  const memoryIndex = spawn("openclaw", ["memory", "index", "--path", EEG_OUTPUT]);

  memoryIndex.stdout.on('data', (data) => {
    console.log("[OpenClaw Memory Indexing]: " + data.toString());
  });

  memoryIndex.stderr.on('data', (data) => {
    console.error("[OpenClaw Memory Error]: " + data.toString());
  });

  memoryIndex.on('close', (code) => {
    if (code === 0) {
      console.log("EEG thoughts successfully indexed to memory and vector search.");
    } else {
      console.log("Memory indexing process exited with code " + code + ". Check logs for more info.");
    }
  });
}

// Start script
console.log("braindecode skill initialized! Watching for EEG data...");