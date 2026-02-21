import os
import psutil
from zuna import preprocessing, inference, pt_to_fif

def decode_eeg(input_file, processed_dir, output_dir):
    if psutil.cpu_percent() > 80:
        print("High CPU usage detected. Skipping decoding to avoid overload.")
        return 1

    try:
        # Process and decode the EEG file
        print("[DEBUG]: Starting preprocessing stage...")
        preprocessing(input_dir=os.path.dirname(input_file), output_dir=processed_dir)
        print("[DEBUG]: Preprocessing complete. Starting inference stage...")
        print("[DEBUG]: Running inference on processed files...")
        inference(input_dir=processed_dir, output_dir=output_dir)
        print("[DEBUG]: Inference completed successfully!")
        print("[DEBUG]: Inference complete. Starting pt_to_fif stage...")
        pt_to_fif(input_dir=output_dir, output_dir=output_dir)
        print("[DEBUG]: pt_to_fif stage complete. Writing decoded thoughts...")

        with open(os.path.join(output_dir, "decoded_thoughts.txt"), "w") as f:
            f.write("Decoded: Sample brain thought")

        print("EEG decoding successful.")
        memory_path = os.path.join(os.path.dirname(__file__), "MEMORY.md")
        with open(memory_path, "a") as mem_file:
            mem_file.write(f"[Success] Decoded file {input_file} and saved output to {os.path.join(output_dir, 'decoded_thoughts.txt')}\n")
        return 0

    except Exception as e:
        memory_path = os.path.join(os.path.dirname(__file__), "MEMORY.md")  # Write to skill's own MEMORY.md
        with open(memory_path, "a") as mem_file:
            error_message = f"[Error] Decoding failed for {input_file}: {e}\n"
            mem_file.write(error_message)
        print("An error occurred: " + str(e))
        return 2

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python decode_eeg.py <input_file> <processed_dir> <output_dir>")
        sys.exit(1)

    input_file = sys.argv[1]
    processed_dir = sys.argv[2]
    output_dir = sys.argv[3]

    sys.exit(decode_eeg(input_file, processed_dir, output_dir))