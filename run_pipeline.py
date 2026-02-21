#!/usr/bin/env python3
"""
Zuna Pipeline

Runs the complete EEG reconstruction pipeline:
1. Preprocessing: .fif → .pt (filtered, epoched, normalized)
2. Inference: .pt → .pt (reconstructed by model)
3. Reconstruction: .pt → .fif (denormalized, continuous)
4. Visualization: comparison plots (optional)

Edit the paths and options below, then run:
python run_zuna_pipeline.py

For documentation on each function, run:
    help(zuna.preprocessing)
    help(zuna.inference)
    help(zuna.pt_to_fif)
    help(zuna.compare_plot_pipeline)
"""

import os
import shutil
from pathlib import Path
os.environ['TORCH_DISTRIBUTED_PORT'] = '29500'
from zuna import preprocessing, inference, pt_to_fif, compare_plot_pipeline

# =============================================================================
# PATHS & OPTIONS
# =============================================================================
TUTORIAL_DIR = Path(__file__).parent.resolve()
INPUT_DIR = str(TUTORIAL_DIR / "eeg-input")
WORKING_DIR = str(TUTORIAL_DIR / "temp-working")

# Derived paths (nested directory structure)
WORKING_PATH = Path(WORKING_DIR)
PREPROCESSED_FIF_DIR = str(WORKING_PATH / "1_preprocessed")
PT_INPUT_DIR = str(WORKING_PATH / "2_processed")
PT_OUTPUT_DIR = str(WORKING_PATH / "3_inferred")
FIF_OUTPUT_DIR = str(WORKING_PATH / "4_decoded")
FIGURES_DIR = str(WORKING_PATH / "figures")

# Create working directories
for d in [PREPROCESSED_FIF_DIR, PT_INPUT_DIR, PT_OUTPUT_DIR, FIF_OUTPUT_DIR]:
    Path(d).mkdir(parents=True, exist_ok=True)

# =============================================================================
# OPTIONS
# =============================================================================
APPLY_NOTCH_FILTER = False  # Remove power line interference if needed
APPLY_HIGHPASS_FILTER = True  # Apply high-pass filter for drift removal
APPLY_AVERAGE_REFERENCE = True  # Convert to average reference montage
BAD_CHANNELS = []  # Channels to zero-out artifacts
TARGET_CHANNEL_COUNT = None  # No upsampling
DROP_BAD_CHANNELS = False  # Detect and remove bad channels
DROP_BAD_EPOCHS = False  # Detect and remove bad epochs
ZERO_OUT_ARTIFACTS = False  # Zero-out artifact samples
GPU_DEVICE = ""  # Default GPU to use
TOKENS_PER_BATCH = 5000  # GPU utilization optimization
DATA_NORM = 10.0  # Data normalization for Zuna expectations
DIFFUSION_CFG = 1.0
DIFFUSION_SAMPLE_STEPS = 5
PLOT_EEG_SIGNAL_SAMPLES = True
PLOT_PT_COMPARISON = True
PLOT_FIF_COMPARISON = True
KEEP_INTERMEDIATE_FILES = True
NUM_SAMPLES = 2

# Pipeline Code
if __name__ == "__main__":
    # Step 1: Preprocessing (.fif → .pt)
    print("[1/4] Preprocessing...", flush=True)
    preprocessing(
        input_dir=INPUT_DIR,
        output_dir=PT_INPUT_DIR,
        apply_notch_filter=APPLY_NOTCH_FILTER,
        apply_highpass_filter=APPLY_HIGHPASS_FILTER,
        apply_average_reference=APPLY_AVERAGE_REFERENCE,
        preprocessed_fif_dir=PREPROCESSED_FIF_DIR,
        drop_bad_channels=DROP_BAD_CHANNELS,
        drop_bad_epochs=DROP_BAD_EPOCHS,
        zero_out_artifacts=ZERO_OUT_ARTIFACTS,
        target_channel_count=TARGET_CHANNEL_COUNT,
        bad_channels=BAD_CHANNELS,
    )
    # Step 2: Model Inference (.pt → .pt)
    print("[2/4] Model inference...", flush=True)
    inference(
        input_dir=PT_INPUT_DIR,
        output_dir=PT_OUTPUT_DIR,
        gpu_device=GPU_DEVICE,
        tokens_per_batch=TOKENS_PER_BATCH,
        data_norm=DATA_NORM,
        diffusion_cfg=DIFFUSION_CFG,
        diffusion_sample_steps=DIFFUSION_SAMPLE_STEPS,
        plot_eeg_signal_samples=PLOT_EEG_SIGNAL_SAMPLES,
    )
    # Step 3: Reconstruction (.pt → .fif)
    print("[3/4] Reconstructing FIF files...", flush=True)
    pt_to_fif(
        input_dir=PT_OUTPUT_DIR,
        output_dir=FIF_OUTPUT_DIR,
    )
    # Step 4: Visualization
    print("[4/4] Generating comparison plots...", flush=True)
    compare_plot_pipeline(
        input_dir=INPUT_DIR,
        fif_input_dir=PREPROCESSED_FIF_DIR,
        fif_output_dir=FIF_OUTPUT_DIR,
        pt_input_dir=PT_INPUT_DIR,
        pt_output_dir=PT_OUTPUT_DIR,
        output_dir=FIGURES_DIR,
        plot_pt=PLOT_PT_COMPARISON,
        plot_fif=PLOT_FIF_COMPARISON,
        num_samples=NUM_SAMPLES,
    )
    print("Pipeline execution completed successfully.")