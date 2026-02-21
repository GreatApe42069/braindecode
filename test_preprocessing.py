import os
from zuna.preprocessing import preprocessing

# Paths
input_dir = "/home/greatape42069/.openclaw/eeg-input"
processed_dir = "/home/greatape42069/.openclaw/eeg-processed"
output_dir = "/home/greatape42069/.openclaw/eeg-output"

# Ensure processed and output directories exist
os.makedirs(processed_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

# Perform preprocessing on the sample_raw.fif file
results = preprocessing(
    input_dir=input_dir,
    output_dir=processed_dir,
    apply_notch_filter=True,
    apply_highpass_filter=True,
    apply_average_reference=True,
    save_preprocessed_fif=True,
    n_jobs=1
)

# Output preprocessing results
print("Preprocessing Results:")
print(results)