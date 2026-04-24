# Ashley Voice Testing Guide

Complete guide to test the Azure Ashley voice replica with Kokoro TTS and E-core optimization.

## Prerequisites

1. **Install Kokoro TTS with dependencies**:
   ```bash
   cd d:\AICompanionProject\kokoro-tts-2.3.1
   pip install -e .
   ```
   This installs:
   - `librosa` (pitch shifting)
   - `psutil` (E-core affinity)
   - `kokoro-onnx` (TTS engine)

2. **Verify dependencies installed**:
   ```bash
   python -c "import librosa; import psutil; print('✓ Dependencies OK')"
   ```

---

## Test 1: Basic Ashley Voice Output

**Test if the voice sounds like Azure Ashley (warm, clear, pitched up)**

```bash
# Simple test
kokoro-tts "Hello, I'm Ashley. This is the neuro vtuber voice." --voice ashley_neuro

# Output to file for comparison
kokoro-tts "Hello, I'm Ashley. How are you today?" --voice ashley_neuro -o ashley_test.wav
```

**Expected**:
- Audio file created
- Voice sounds warm, clear, female
- Pitch noticeably higher than normal (~25% up)
- ~2-5 second latency for processing

**Troubleshooting**:
- If no output: Check model files exist (`kokoro-v1.0.onnx`, `voices-v1.0.bin`)
- If error about librosa: Run `pip install librosa>=0.10.0`
- If voice sounds wrong: Verify blend uses `af_sarah:70,af_bella:30`

---

## Test 2: E-core Affinity Verification

**Test if Kokoro locks to E-cores (16-23 on i9-13900KS)**

**Create test script** `test_ecores.py`:
```python
#!/usr/bin/env python3
import os
import psutil
import subprocess

# Show initial affinity
print("Testing E-core affinity for Kokoro TTS...\n")
print(f"Available CPUs: {psutil.cpu_count(logical=True)} logical cores")
print(f"Main process affinity: {sorted(psutil.Process(os.getpid()).cpu_affinity())}")

# Run Kokoro with simple text
cmd = [
    "kokoro-tts",
    "Testing E-core affinity with a short sentence.",
    "--voice", "ashley_neuro",
    "-o", "test_ecores_output.wav"
]

print(f"\nRunning: {' '.join(cmd)}\n")
proc = subprocess.Popen(cmd)

# Monitor child process affinity
import time
time.sleep(0.5)  # Give it time to start

try:
    parent = psutil.Process(proc.pid)
    for child in parent.children(recursive=True):
        affinity = child.cpu_affinity()
        print(f"Child process {child.pid} affinity: {sorted(affinity)}")
        if all(16 <= cpu <= 23 for cpu in affinity):
            print("  ✓ Locked to E-cores (16-23)")
        else:
            print("  ✗ NOT locked to E-cores")
except:
    pass

proc.wait()
print("\nDone.")
```

**Run it**:
```bash
python test_ecores.py
```

**Expected**:
- Child process affinity shows cores 16-23 only
- Output: `✓ Locked to E-cores (16-23)`
- `test_ecores_output.wav` created successfully

---

## Test 3: Voice Comparison (Ashley vs Standard)

**Compare ashley_neuro vs plain af_sarah to verify pitch shift**

```bash
# Generate with ashley_neuro (blended + pitched)
kokoro-tts "The quick brown fox jumps over the lazy dog." --voice ashley_neuro -o ashley_neuro.wav

# Generate with plain af_sarah (no pitch shift)
kokoro-tts "The quick brown fox jumps over the lazy dog." --voice af_sarah -o af_sarah.wav

# Generate with plain af_bella (softer)
kokoro-tts "The quick brown fox jumps over the lazy dog." --voice af_bella -o af_bella.wav
```

**Compare manually**:
- Play each in media player
- ashley_neuro should sound:
  - Noticeably higher pitched than both af_sarah and af_bella
  - Warmer tone (blend effect)
  - Clearer (sarah-dominant)

---

## Test 4: Streaming (Real-time Playback)

**Test streaming with E-core efficiency**

```bash
# Create a longer text file
echo "Hello, I'm Ashley, your AI vtuber voice. I can speak naturally with pitch and warmth. 
Testing the streaming capability to see latency and quality. This demonstrates real-time 
speech synthesis with E-core optimization on your i9-13900KS CPU." > test_stream.txt

# Stream with ashley_neuro
kokoro-tts test_stream.txt --voice ashley_neuro --stream
```

**Expected**:
- Audio starts playing ~1-2 seconds after command (first chunk synthesis)
- Continuous playback with minimal gaps
- Warm, clear voice at higher pitch

---

## Test 5: CPU Affinity Module Direct Test

**Verify the cpu_affinity module works**

```bash
python -c "
from kokoro_tts.cpu_affinity import set_e_core_affinity, get_current_affinity
print('Testing CPU affinity module...')
result = set_e_core_affinity()
print(f'E-core affinity set: {result}')
print(f'Current affinity: {get_current_affinity()}')
if result and get_current_affinity() == list(range(16, 24)):
    print('✓ E-core module works!')
else:
    print('✗ E-core module failed or not locked to 16-23')
"
```

**Expected**:
- `E-core affinity set: True`
- `Current affinity: [16, 17, 18, 19, 20, 21, 22, 23]`
- `✓ E-core module works!`

---

## Test 6: Integration with Talk-LLaMA

**Test using ashley_neuro with the speak script**

```bash
# Create test text
echo "Ashley is the AI vtuber voice from Azure, now optimized locally." > test_talk.txt

# Use speak script with ashley_neuro
cd d:\AICompanionProject\whisper.cpp\examples\talk-llama
bash speak ashley_neuro ../../test_talk.txt
```

**Expected**:
- Audio plays through your default speaker
- Voice is warm, clear, high-pitched (Ashley characteristics)
- No ffplay/playback errors

---

## Test 7: Pitch Shift Verification (Advanced)

**Measure actual pitch shift with librosa**

```python
#!/usr/bin/env python3
import librosa
import numpy as np
import soundfile as sf

# Load both files
ashley, sr_ashley = librosa.load('ashley_neuro.wav')
sarah, sr_sarah = librosa.load('af_sarah.wav')

# Estimate pitch
def estimate_pitch(audio, sr, fmin=50, fmax=300):
    F0 = librosa.yin(audio, fmin=fmin, fmax=fmax, sr=sr)
    median_f0 = np.nanmedian(F0[F0 > 0])
    return median_f0

f0_ashley = estimate_pitch(ashley, sr_ashley)
f0_sarah = estimate_pitch(sarah, sr_sarah)

print(f"Ashley pitch (Hz): {f0_ashley:.1f}")
print(f"Sarah pitch (Hz): {f0_sarah:.1f}")

if f0_ashley > 0 and f0_sarah > 0:
    ratio = f0_ashley / f0_sarah
    semitones = 12 * np.log2(ratio)
    print(f"Pitch shift: {semitones:.1f} semitones ({ratio:.2f}x ratio)")
    print(f"Expected: ~+6 semitones (1.41x ratio)")
    if 5 <= semitones <= 7:
        print("✓ Pitch shift is correct!")
    else:
        print("✗ Pitch shift may be incorrect")
```

---

## Performance Benchmarks

Expected performance on i9-13900KS with E-core affinity:

| Metric | Value |
|--------|-------|
| First chunk latency | 2-3 seconds |
| Chunk processing (1000 chars) | 1-2 seconds |
| CPU usage (E-cores only) | 40-60% |
| Memory | ~300-400 MB |
| Streaming latency | <1 second between chunks |

---

## Troubleshooting

### "kokoro-tts command not found"
```bash
pip install -e d:\AICompanionProject\kokoro-tts-2.3.1
# Or add to PATH:
set PATH=%PATH%;d:\AICompanionProject\kokoro-tts-2.3.1\kokoro_tts
```

### "ModuleNotFoundError: No module named 'librosa'"
```bash
pip install librosa>=0.10.0
```

### "ModuleNotFoundError: No module named 'psutil'"
```bash
pip install psutil>=5.9.0
```

### "Error: Unsupported voice: ashley_neuro"
- Check kokoro_tts/__init__.py validate_voice() has the ashley_neuro handler
- Verify line 262 has: `if voice == "ashley_neuro": return "ashley_neuro"`

### Audio sounds wrong / not pitched up
- Verify process_chunk_sequential has pitch shift code (line ~755-770)
- Check `apply_ashley_voice()` is being called with `n_steps=6`
- Regenerate audio file to test

### E-core affinity not working
- Check psutil installed: `pip install psutil>=5.9.0`
- Verify cpu_affinity.py exists and is imported in __init__.py
- Check your CPU core count: `python -c "import psutil; print(psutil.cpu_count())"`

---

## Quick Test Command

**All-in-one verification**:
```bash
python -c "
import subprocess
import sys

tests = [
    ('kokoro-tts --help', 'CLI available'),
    ('python -c \"import librosa\"', 'librosa installed'),
    ('python -c \"import psutil\"', 'psutil installed'),
]

for cmd, name in tests:
    try:
        subprocess.run(cmd, shell=True, capture_output=True, check=True)
        print(f'✓ {name}')
    except:
        print(f'✗ {name}')

# Try generating
print('\\nGenerating test audio...')
result = subprocess.run(
    'kokoro-tts \"Testing Ashley voice.\" --voice ashley_neuro -o test.wav',
    shell=True,
    capture_output=True
)
if result.returncode == 0:
    print('✓ Ashley voice generation works')
else:
    print('✗ Ashley voice generation failed')
    print(result.stderr.decode())
"
```

---

## What Each Test Verifies

| Test | Verifies |
|------|----------|
| Test 1 | Basic voice output & pitch shift |
| Test 2 | E-core CPU affinity locking |
| Test 3 | Voice blend & pitch shift quality |
| Test 4 | Streaming mode & latency |
| Test 5 | CPU affinity module functionality |
| Test 6 | Integration with talk-llama pipeline |
| Test 7 | Actual pitch shift measurements |
