from kokoro_onnx import Kokoro
import soundfile as sf

# Initialize Kokoro
# Ensure these files are in the same directory as this script
kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")

text = "This is a smoke test to verify the Kokoro voice model."

# Generate audio
# 'af_sky' is a standard American Female voice included in the bin file
samples, sample_rate = kokoro.create(
    text, 
    voice="af_sky", 
    speed=1.0, 
    lang="en-us"
)
    
# Save to file
sf.write("smoke_test.wav", samples, sample_rate)

print("Smoke test successful! Audio saved to 'smoke_test.wav'")