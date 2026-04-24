# Ashley Voice - Pre-Testing Checklist

Complete this checklist before running tests to ensure everything is set up correctly.

## ✅ System Check

- [ ] Windows 11 Pro (confirmed)
- [ ] i9-13900KS (confirmed)
- [ ] Python 3.11+ installed
- [ ] Git available (optional)
- [ ] At least 1 GB free RAM
- [ ] At least 500 MB free disk space

**Check Python version:**
```bash
python --version  # Should show 3.11 or higher
```

---

## ✅ Installation Check

- [ ] Kokoro TTS directory accessible: `d:\AICompanionProject\kokoro-tts-2.3.1\`
- [ ] Git working directory initialized
- [ ] Model files exist:
  - [ ] `kokoro-v1.0.onnx` (if not, will download)
  - [ ] `voices-v1.0.bin` (if not, will download)

**Check model files:**
```bash
cd d:\AICompanionProject\kokoro-tts-2.3.1
dir kokoro-*.onnx voices-*.bin
```

---

## ✅ Dependencies Check

Run each command and verify it shows a version number:

- [ ] Python: `python --version`
- [ ] Pip: `pip --version`
- [ ] Setuptools: `pip show setuptools`

**Install base Kokoro:**
```bash
cd d:\AICompanionProject\kokoro-tts-2.3.1
pip install -e .
```

**Verify core dependencies:**
```bash
python -c "import kokoro_onnx; print('✓ kokoro_onnx OK')"
python -c "import soundfile; print('✓ soundfile OK')"
python -c "import sounddevice; print('✓ sounddevice OK')"
python -c "import numpy; print('✓ numpy OK')"
```

**Verify new dependencies:**
```bash
python -c "import librosa; print('✓ librosa OK')"
python -c "import psutil; print('✓ psutil OK')"
```

- [ ] All dependencies import successfully

---

## ✅ Module Check

Verify the modified/created modules exist:

**Check main module:**
- [ ] `kokoro_tts/__init__.py` exists
- [ ] File contains: `from .cpu_affinity import set_e_core_affinity` (line ~28)
- [ ] File contains: `def pitch_shift_audio()` (line ~107)
- [ ] File contains: `def apply_ashley_voice()` (line ~119)
- [ ] File contains: `set_e_core_affinity()` in main() (line ~1304)

**Check CPU affinity module:**
- [ ] `kokoro_tts/cpu_affinity.py` exists (new file)
- [ ] File contains: `def set_e_core_affinity()`
- [ ] File contains: `def get_current_affinity()`
- [ ] File is importable: 
  ```bash
  python -c "from kokoro_tts.cpu_affinity import set_e_core_affinity; print('✓ OK')"
  ```

**Check test scripts exist:**
- [ ] `test_1_basic_ashley.py` exists
- [ ] `test_2_ecores.py` exists
- [ ] `test_3_voice_comparison.py` exists
- [ ] `test_4_cpu_affinity.py` exists
- [ ] `test_5_streaming.py` exists
- [ ] `test_6_pitch_shift.py` exists
- [ ] `run_all_tests.py` exists

---

## ✅ Integration Check

**Check speak script update:**
```bash
grep -n "ashley_neuro" d:\AICompanionProject\whisper.cpp\examples\talk-llama\speak
```
- [ ] Should show ashley_neuro support added

**Check pyproject.toml:**
```bash
grep -E "librosa|psutil" d:\AICompanionProject\kokoro-tts-2.3.1\pyproject.toml
```
- [ ] Should show both librosa and psutil in dependencies

---

## ✅ Quick Functionality Check

**Test 1: Basic command**
```bash
kokoro-tts "Test" --voice ashley_neuro -o quick_test.wav
```
- [ ] Command completes without error
- [ ] File `quick_test.wav` created
- [ ] File size > 10 KB

**Test 2: E-core module**
```bash
python -c "
from kokoro_tts.cpu_affinity import set_e_core_affinity, get_current_affinity
result = set_e_core_affinity()
affinity = get_current_affinity()
print(f'Set result: {result}')
print(f'Affinity: {affinity}')
if all(16 <= c <= 23 for c in affinity):
    print('✓ E-cores locked')
else:
    print('! E-cores not fully locked')
"
```
- [ ] Shows: `Set result: True`
- [ ] Shows affinity in range 16-23

**Test 3: Voice validation**
```bash
python -c "
from kokoro_onnx import Kokoro
kokoro = Kokoro()
from kokoro_tts import validate_voice
result = validate_voice('ashley_neuro', kokoro)
print(f'Validation result: {result}')
if result == 'ashley_neuro':
    print('✓ ashley_neuro preset recognized')
"
```
- [ ] Shows: `Validation result: ashley_neuro`

---

## ✅ Audio Equipment Check

- [ ] Speakers/headphones connected
- [ ] System volume not muted
- [ ] Audio output device working

**Test audio output:**
```bash
# Generate and play a test tone
python -c "
import numpy as np
import sounddevice as sd
sample_rate = 24000
frequency = 440  # A note
duration = 1
t = np.arange(duration * sample_rate) / sample_rate
tone = 0.3 * np.sin(2 * np.pi * frequency * t)
sd.play(tone, sample_rate)
sd.wait()
print('✓ Audio output working')
"
```
- [ ] You hear a 1-second tone

---

## ✅ Documentation Check

- [ ] README_TESTING.md exists
- [ ] QUICK_TEST_REFERENCE.md exists
- [ ] ASHLEY_TESTING_GUIDE.md exists
- [ ] IMPLEMENTATION_SUMMARY.md exists
- [ ] ARCHITECTURE_DIAGRAM.md exists

---

## ✅ Disk Space Check

Required space:
- [ ] ~500 MB for Python packages
- [ ] ~100 MB for Kokoro models
- [ ] ~200 MB working space for test files

**Check free space:**
```bash
dir d:\
# Check free space on D: drive
```

---

## ✅ Permission Check

- [ ] Can read/write in `d:\AICompanionProject\kokoro-tts-2.3.1\`
- [ ] Can execute Python scripts
- [ ] Can create files in working directory

**Test write permissions:**
```bash
cd d:\AICompanionProject\kokoro-tts-2.3.1
echo "test" > permission_test.txt
del permission_test.txt
```
- [ ] Both commands succeed

---

## ✅ Pre-Flight Summary

Count checkmarks:
- System checks: ___/3
- Installation checks: ___/3
- Dependency checks: ___/6
- Module checks: ___/10
- Integration checks: ___/3
- Functionality checks: ___/3
- Audio checks: ___/3
- Documentation checks: ___/5
- Disk space checks: ___/3
- Permission checks: ___/3

**Total: ___/42 checks**

---

## 🚀 Ready to Test!

If you have **40+/42 checks**, you're ready!

**Next steps:**
1. Run: `python test_1_basic_ashley.py`
2. Listen to output file
3. Run: `python run_all_tests.py` for comprehensive verification
4. Check **QUICK_TEST_REFERENCE.md** for next steps

---

## ⚠️ If Checks Fail

### Issue: Dependencies not installing
**Solution:**
```bash
pip install --upgrade pip
pip install setuptools wheel
pip install -e d:\AICompanionProject\kokoro-tts-2.3.1 --force-reinstall
```

### Issue: Model files missing
**Solution:**
```bash
# Kokoro will auto-download on first run, OR manually:
# Download kokoro-v1.0.onnx and voices-v1.0.bin
# Place in d:\AICompanionProject\kokoro-tts-2.3.1\
```

### Issue: E-core module not found
**Solution:**
```bash
# Reinstall in editable mode
cd d:\AICompanionProject\kokoro-tts-2.3.1
pip install -e . --force-reinstall --no-deps
```

### Issue: Audio not working
**Solution:**
```bash
# Check audio device
python -c "import sounddevice; print(sounddevice.query_devices())"
# Verify speakers in Windows Sound settings
```

---

## 📋 Recheck After Fixes

After fixing any issue, re-run the relevant check section above.

---

**Checklist Version**: 1.0  
**Last Updated**: 2026-04-24  
**Status**: Ready for testing  

Good luck! 🚀
