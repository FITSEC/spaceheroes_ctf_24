import numpy as np
from scipy.io.wavfile import read

def decode_ask(signal, sample_rate=44100, freq=1000, duration_per_bit=0.01):
    """
    Decode ASK-encoded signal back to text.

    Parameters:
    - signal: The ASK-modulated signal as a numpy array.
    - sample_rate: Samples per second used in the encoding.
    - freq: Frequency of the carrier signal used in the encoding.
    - duration_per_bit: Duration of each bit in seconds.

    Returns:
    - The decoded text.
    """
    bits_per_sample = int(sample_rate * duration_per_bit)
    num_bits = len(signal) // bits_per_sample
    decoded_bits = ''

    for i in range(num_bits):
        # Extract the slice of the signal corresponding to this bit
        start = i * bits_per_sample
        end = start + bits_per_sample
        sample = signal[start:end]

        # Use the average amplitude of the sample to decide if it's a 1 or a 0
        avg_amplitude = np.abs(sample).mean()
        if avg_amplitude > signal.max() / 3:  # Adjust this threshold as needed
            decoded_bits += '1'
        else:
            decoded_bits += '0'

    # Convert the binary string to ASCII text
    text = ''.join(chr(int(decoded_bits[i:i+8], 2)) for i in range(0, len(decoded_bits), 8))

    return text

def read_ask_from_wav(filename):
    """
    Read ASK-encoded WAV file and decode it to text.

    Parameters:
    - filename: Name of the input WAV file.

    Returns:
    - The decoded text.
    """
    sample_rate, signal = read(filename)
    signal = signal / 32767.0  # Normalize back to range used in encoding
    return decode_ask(signal, sample_rate)

# Example usage
if __name__ == "__main__":
    decoded_text = read_ask_from_wav("text_encoded.wav")
    print(decoded_text)

