import numpy as np
from scipy.io.wavfile import write

def text_to_ask(text, sample_rate=44100, freq=1000, duration_per_bit=0.01):
    """
    Encode text using ASK and generate a signal.

    Parameters:
    - text: The text to encode.
    - sample_rate: Samples per second.
    - freq: Frequency of the carrier signal.
    - duration_per_bit: Duration of each bit in seconds.

    Returns:
    - A numpy array containing the ASK-encoded signal.
    """
    bits = ''.join(format(ord(char), '08b') for char in text)  # Convert text to binary
    t = np.linspace(0, duration_per_bit, int(sample_rate * duration_per_bit), endpoint=False)
    signal = np.array([])

    for bit in bits:
        if bit == '1':
            amplitude = 1
        else:
            amplitude = 0.5  # Change this as per your encoding scheme
        sine_wave = amplitude * np.sin(2 * np.pi * freq * t)
        signal = np.concatenate((signal, sine_wave))

    return signal

def write_ask_to_wav(text, filename="output.wav", sample_rate=44100, freq=1000, duration_per_bit=0.01):
    """
    Convert text to ASK, then write to a WAV file.

    Parameters:
    - text: The text to encode.
    - filename: Name of the output WAV file.
    - sample_rate, freq, duration_per_bit: Parameters for the ASK signal.
    """
    signal = text_to_ask(text, sample_rate, freq, duration_per_bit)
    # Normalize to 16-bit range
    signal_normalized = np.int16((signal / signal.max()) * 32767)
    write(filename, sample_rate, signal_normalized)

# Example usage
if __name__ == "__main__":
    with open("input.txt", "r") as file:
        text = file.read()

    write_ask_to_wav(text, "text_encoded.wav")
