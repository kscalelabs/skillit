import librosa
import noisereduce as nr
import soundfile as sf

# Load the audio file
audio, sr = librosa.load('recorded_audio.wav', sr=None)

# Estimate noise using a silent portion of the audio
noise_sample = audio[:int(sr * 1)]  # First second assumed to be noise

# Apply noise reduction
reduced_noise = nr.reduce_noise(y=audio, y_noise=noise_sample, sr=sr)

# Save the output
sf.write('recorded_audio.wav', reduced_noise, sr)
