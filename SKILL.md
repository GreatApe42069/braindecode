# braindecode Skill

## Overview
The `braindecode` skill integrates brain-computer interface (BCI) technology into your OpenClaw agent, enabling decoding of EEG (electroencephalogram) signals into actionable text. These decoded thoughts are seamlessly integrated into your agent's semantic memory and vector search system. This skill allows you to control your agent using brain signals.

---

## Features
- Real-time EEG data monitoring and processing.
- Decodes EEG signals into meaningful text using the ZUNA model from Hugging Face.
- Indexed outputs in OpenClaw’s semantic memory and FTS5 vector database.
- Fault-tolerant: Monitors system resources and safely handles high CPU/low performance scenarios.
- Local-first processing: Data is not sent to external servers, ensuring full privacy.

---

## Installation

1. **Prerequisites:**
   - Python 3.14.2 or later installed on your system.
   - Ensure `pip` is available.
   - `pnpm` is required to manage the skill.

2. Run the following commands to install the skill:
   ```bash
   npx clawhub@latest install braindecode
   cd ~/.openclaw/skills/braindecode
   pnpm run install-skill
   ```
   
3. **What it Does:**
   - Sets up the necessary EEG directories in `~/.openclaw`.
   - Installs ZUNA and other Python dependencies (`torch`, `mne`, etc.).
   - Downloads the ZUNA model from Hugging Face.
   - Configures `openclaw.json` for EEG inputs.
   - Enables the `bci-core` plugin in OpenClaw.
   - Restarts the OpenClaw Gateway to apply changes.

---

## Usage

### Activating Brain Mode
1. **Command:** Simply tell your agent
   > *"Enable brain mode."*

   This will activate the skill, start monitoring the EEG input directory, and decode brain signals in near real-time.

2. Place EEG `.fif` files in `~/.openclaw/eeg-input/`. Each file triggers automatic decoding when saved to the directory.

3. Once processed:
   - Decoded thoughts are saved to `~/.openclaw/eeg-output/`.
   - Indexed into semantic memory for retrieval.
   - Agent responds with the decoded thoughts (e.g., *"Woof! Your brain says: Check Doge wallet balance."*)

---

### Monitoring
- **HEARTBEAT Monitoring:**
  - The skill appends a check to your `HEARTBEAT.md`, which monitors ZUNA inference latency and resource usage every 60 seconds.
  - If inference fails due to high system load or other issues, the skill logs errors into `MEMORY.md`.

---

## Troubleshooting
### Common Issues
- **High CPU Usage:**
  - If CPU usage exceeds 80%, the skill skips processing to avoid system instability.
  - Logs a resource usage warning in `HEARTBEAT.md` and `MEMORY.md`.
- **ZUNA Dependency Issues:**
  - Re-run the install script: `pnpm run install-skill`.
  - Ensure Python 3 and pip are correctly configured.

---

### Logs
- All key events, errors, and decoded output are logged to OpenClaw’s `MEMORY.md` file.
- Check logs and resource usage for troubleshooting irregular task behavior.
  ```bash
  tail -f ~/.openclaw/workspace/logs/system_monitor
  ```

---

### Skill Updates
- To update the skill: Re-run the install script using `pnpm run install-skill`.
- Check ClawHub for updates: `npx clawhub@latest update braindecode`.

---

## Contributing and Testing

1. **Testing:**
   - Test the skill by manually dropping `.fif` files (example files from ZUNA).
   - Use debug logging in HEARTBEAT.md to verify functionality.

2. **Contributing:**
   - Fork the `braindecode` repository on ClawHub.
   - PRs with error-handling or performance improvements are welcome!

---

Reach out to Degen Doge for more guidance! 🧠🐕