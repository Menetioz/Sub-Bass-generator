import os
import numpy as np
import sounddevice as sd
import soundfile as sf
import tkinter as tk
from tkinter import filedialog

def generate_punchy_808_sub_bass(duration, frequency, amplitude, sample_rate):
    t = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)

    # Envelope shaping
    attack_time = 0.01
    decay_time = 0.2
    sustain_level = 0.5
    release_time = 0.01

    # Generate the sub bass waveform
    waveform = np.zeros_like(t)
    mask = np.logical_and(t >= attack_time + decay_time, t < duration - release_time)
    waveform[mask] = sustain_level * np.sin(2 * np.pi * frequency * t[mask])

    # Attack
    attack_samples = int(attack_time * sample_rate)
    attack_curve = np.linspace(0.0, 1.0, attack_samples)
    waveform[:attack_samples] *= attack_curve

    # Decay
    decay_samples = int(decay_time * sample_rate)
    decay_curve = np.linspace(1.0, sustain_level, decay_samples)
    waveform[attack_samples:attack_samples + decay_samples] *= decay_curve

    # Release
    release_samples = int(release_time * sample_rate)
    release_curve = np.linspace(sustain_level, 0.0, release_samples)
    waveform[-release_samples:] *= release_curve

    # Apply pitch slide
    slide_time = 0.05
    slide_samples = int(slide_time * sample_rate)
    slide_curve = np.linspace(1.0, 0.5, slide_samples)
    waveform[:slide_samples] *= slide_curve

    # Apply distortion for texture
    waveform = np.tanh(waveform)

    return amplitude * waveform

def generate_punchy_808_sub_bass_sounds():
    num_sounds = int(num_sounds_entry.get())

    # Parameters for the sub bass
    duration = 1.0  # Duration in seconds
    sample_rate = 44100  # Sample rate (standard for audio)

    # Create "subs" folder if it doesn't exist
    if not os.path.exists("subs"):
        os.makedirs("subs")

    for i in range(num_sounds):
        # Randomly generate frequency and amplitude for each sub bass sound
        frequency = np.random.uniform(30.0, 80.0)  # Random frequency between 30 and 80 Hz
        amplitude = np.random.uniform(0.5, 1.0)  # Random amplitude between 0.5 and 1.0

        # Generate the punchy 808 sub bass waveform
        sub_bass = generate_punchy_808_sub_bass(duration, frequency, amplitude, sample_rate)

        # Export the sub bass sound as a WAV file
        filename = f"subs/808_sub_bass_{i + 1}.wav"
        sf.write(filename, sub_bass, sample_rate)

        print(f"808 Sub bass {i + 1} generated and exported as {filename}")

    print("All 808 sub bass sounds generated and exported.")

    # Prompt for folder selection to store the WAV files
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if output_folder:
        output_path = os.path.join(output_folder, "subs")
        os.makedirs(output_path, exist_ok=True)
        for i in range(num_sounds):
            src_file = f"subs/808_sub_bass_{i + 1}.wav"
            dest_file = os.path.join(output_path, f"punchy_808_sub_bass_{i + 1}.wav")
            os.replace(src_file, dest_file)
        print(f"All punchy 808 sub bass sounds moved to: {output_path}")

# Create the GUI window
window = tk.Tk()
window.title("808 Sub Bass Generator")

# Number of sub bass sounds input
num_sounds_label = tk.Label(window, text="Number of 808 :")
num_sounds_label.pack()

num_sounds_entry = tk.Entry(window)
num_sounds_entry.pack()

# Generate button
generate_button = tk.Button(window, text="Generate", command=generate_punchy_808_sub_bass_sounds)
generate_button.pack()

# Run the GUI main loop
window.mainloop()