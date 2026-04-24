# Ashley Voice - Quick Test Reference

## One-Line Quick Test

```bash
kokoro-tts "Hello, I'm Ashley. Testing the neuro vtuber voice." --voice ashley_neuro
```

Expected: Audio plays with warm, clear, high-pitched female voice.

---

## Test Sequence

### Step 1: Verify Installation (5 min)
```bash
# Install dependencies
cd d:\AICompanionProject\kokoro-tts-2.3.1
pip install -e .

# Verify modules
python -c "import librosa; import psutil; print('✓ OK')"

# Try basic command
kokoro-tts "Test." --voice ashley_neuro -o test.wav
```

✓ **Expected**: File `test.wav` created with warm, high-pitched voice

---

### Step 2: Run Automated Tests (15 min)

```bash
cd d:\AICompanionProject\kokoro-tts-2.3.1

# Run individual tests
python test_1_basic_ashley.py        # Basic voice output
python test_2_ecores.py              # E-core affinity
python test_3_voice_comparison.py    # Voice quality
python test_4_cpu_affinity.py        # Module verification
python test_5_streaming.py           # Real-time playback
python test_6_pitch_shift.py         # Pitch measurement

# Or run all at once
python run_all_tests.py
```

✓ **Expected**: Most/all tests pass with `✓ SUCCESS`

---

### Step 3: Listen & Compare (5 min)

After `test_3_voice_comparison.py`:
```bash
# Listen to generated files (Windows)
start compare_ashley_neuro.wav
start compare_af_sarah.wav
```

✓ **Expected**: 
- ashley_neuro: Higher pitched, warmer, clearer
- af_sarah: Lower baseline for comparison

---

### Step 4: Verify E-cores (2 min)

```bash
python -c "
from kokoro_tts.cpu_affinity import set_e_core_affinity, get_current_affinity
set_e_core_affinity()
print(f'Locked to: {get_current_affinity()}')
"
```

✓ **Expected**: `Locked to: [16, 17, 18, 19, 20, 21, 22, 23]`

---

### Step 5: Integration Test (2 min)

```bash
# Test with talk-llama pipeline
cd d:\AICompanionProject\whisper.cpp\examples\talk-llama

echo "Testing Ashley integration with talk-llama." > test.txt
bash speak ashley_neuro test.txt
```

✓ **Expected**: Audio plays through speaker

---

## Voice Characteristics to Verify

✅ **Pitch**: ~25% higher than normal (noticeably high-pitched)
✅ **Tone**: Warm, friendly, clear (blend of af_sarah + af_bella)
✅ **Quality**: No artifacts, smooth synthesis
✅ **Latency**: <5 seconds for typical sentence

---

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| `kokoro-tts: command not found` | `pip install -e d:\AICompanionProject\kokoro-tts-2.3.1` |
| `ModuleNotFoundError: librosa` | `pip install librosa>=0.10.0` |
| `ModuleNotFoundError: psutil` | `pip install psutil>=5.9.0` |
| Voice sounds normal (not pitched) | Check `apply_ashley_voice()` in __init__.py line ~110 |
| E-core not locking | Verify psutil installed, check cpu_affinity.py imported |
| Audio file not created | Check kokoro model files exist in working directory |

---

## Test File Locations

```
d:\AICompanionProject\kokoro-tts-2.3.1\
├── test_1_basic_ashley.py          # Basic generation
├── test_2_ecores.py                # E-core affinity
├── test_3_voice_comparison.py      # Voice quality
├── test_4_cpu_affinity.py          # Module test
├── test_5_streaming.py             # Streaming mode
├── test_6_pitch_shift.py           # Pitch analysis
├── run_all_tests.py                # Master suite
├── ASHLEY_TESTING_GUIDE.md         # Full guide
└── kokoro_tts/
    ├── __init__.py                 # Main with pitch shift
    └── cpu_affinity.py             # E-core module
```

---

## Expected Output

### Successful Test Run
```
✓ Test 1: Basic Ashley Voice Output
  - File: ashley_test.wav (45000 bytes)
  - Voice: Warm, clear, high-pitched

✓ Test 2: E-core Affinity
  - Locked to cores: [16-23]
  - CPU usage: E-cores only

✓ Test 3: Voice Comparison
  - compare_ashley_neuro.wav
  - compare_af_sarah.wav
  - compare_af_bella.wav

✓ Test 4: CPU Affinity Module
  - set_e_core_affinity(): True
  - get_current_affinity(): [16, 17, 18, 19, 20, 21, 22, 23]

✓ Test 5: Streaming
  - Audio plays smoothly
  - Minimal latency

✓ Test 6: Pitch Shift
  - Ashley pitch: 268.5 Hz
  - Sarah pitch: 189.2 Hz
  - Shift: +6.1 semitones ✓
```

---

## Usage Examples

```bash
# Generate audio file
kokoro-tts "Hello, I'm Ashley." --voice ashley_neuro -o ashley.wav

# Stream with real-time playback
kokoro-tts "Long text here..." --voice ashley_neuro --stream

# Different speed
kokoro-tts "Speaking faster." --voice ashley_neuro --speed 1.2 -o faster.wav

# Different language (if supported)
kokoro-tts "Hola, soy Ashley." --voice ashley_neuro --lang es-es -o spanish.wav

# Split long content
kokoro-tts book.txt --voice ashley_neuro --split-output ./chapters
```

---

## Performance Benchmarks (i9-13900KS with E-cores)

| Metric | Value |
|--------|-------|
| First chunk latency | 2-3 sec |
| Chunk processing (1000 chars) | 1-2 sec |
| CPU usage (E-cores only) | 40-60% |
| Memory usage | 300-400 MB |
| Streaming latency | <1 sec between chunks |
| Typical sentence (10-15 words) | 1-3 sec |

---

## Getting Help

- Full guide: `ASHLEY_TESTING_GUIDE.md`
- Source code: `kokoro_tts/__init__.py` (pitch shift at line ~110)
- E-core module: `kokoro_tts/cpu_affinity.py`
- Integration: `whisper.cpp/examples/talk-llama/speak`

Run this to diagnose issues:
```bash
python -c "
import subprocess; import sys
tests = [
    ('kokoro-tts --help', 'CLI'),
    ('python -c \"import librosa\"', 'librosa'),
    ('python -c \"import psutil\"', 'psutil'),
    ('python -c \"import kokoro_onnx\"', 'kokoro_onnx'),
]
print('Diagnostics:')
for cmd, name in tests:
    try:
        subprocess.run(cmd, shell=True, capture_output=True, check=True)
        print(f'  ✓ {name}')
    except: print(f'  ✗ {name}')
"
```
