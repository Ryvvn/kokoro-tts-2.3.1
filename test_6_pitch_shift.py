#!/usr/bin/env python3
"""Test 6: Pitch Shift Verification (Advanced)"""

import sys
import os

def test_pitch_shift():
    print("=" * 60)
    print("TEST 6: Pitch Shift Verification (Advanced)")
    print("=" * 60)

    try:
        import librosa
        import numpy as np
        print("\n✓ librosa and numpy available")
    except ImportError:
        print("\n✗ FAILED: librosa not installed")
        print("  Install: pip install librosa>=0.10.0")
        return False

    # Check if comparison files exist
    ashley_file = "compare_ashley_neuro.wav"
    sarah_file = "compare_af_sarah.wav"

    if not os.path.exists(ashley_file) or not os.path.exists(sarah_file):
        print(f"\n⚠ Required files not found:")
        print(f"  - {ashley_file}")
        print(f"  - {sarah_file}")
        print(f"\nRun test_3_voice_comparison.py first to generate these files")
        return False

    print(f"\n--- Loading Audio Files ---")
    try:
        ashley, sr_ashley = librosa.load(ashley_file)
        sarah, sr_sarah = librosa.load(sarah_file)
        print(f"✓ Ashley file loaded: {len(ashley)} samples @ {sr_ashley} Hz")
        print(f"✓ Sarah file loaded: {len(sarah)} samples @ {sr_sarah} Hz")
    except Exception as e:
        print(f"✗ FAILED to load files: {e}")
        return False

    # Estimate pitch
    print(f"\n--- Estimating Fundamental Frequency (F0) ---")
    try:
        print(f"Analyzing ashley_neuro.wav...")
        F0_ashley = librosa.yin(ashley, fmin=50, fmax=300, sr=sr_ashley)
        f0_ashley = np.nanmedian(F0_ashley[F0_ashley > 0])

        print(f"Analyzing af_sarah.wav...")
        F0_sarah = librosa.yin(sarah, fmin=50, fmax=300, sr=sr_sarah)
        f0_sarah = np.nanmedian(F0_sarah[F0_sarah > 0])

        print(f"\n✓ Pitch estimation complete")
    except Exception as e:
        print(f"✗ FAILED to estimate pitch: {e}")
        return False

    # Compare
    print(f"\n--- Pitch Comparison ---")
    print(f"Ashley pitch: {f0_ashley:.1f} Hz")
    print(f"Sarah pitch:  {f0_sarah:.1f} Hz")

    if f0_ashley > 0 and f0_sarah > 0:
        ratio = f0_ashley / f0_sarah
        semitones = 12 * np.log2(ratio)

        print(f"\nRatio: {ratio:.2f}x")
        print(f"Semitones: {semitones:.1f} semitones")

        print(f"\n--- Verification ---")
        print(f"Expected: +6 semitones (1.41x ratio)")
        print(f"Got:      {semitones:.1f} semitones ({ratio:.2f}x ratio)")

        if 5 <= semitones <= 7:
            print(f"\n✓ SUCCESS: Pitch shift is correct! (+{semitones:.1f} semitones)")
            return True
        else:
            print(f"\n⚠ WARNING: Pitch shift may be incorrect")
            print(f"Expected ~6 semitones, got {semitones:.1f}")
            if semitones < 0:
                print(f"Ashley voice is LOWER than Sarah (should be higher)")
            elif semitones < 3:
                print(f"Pitch shift is too low (expected ~6)")
            elif semitones > 9:
                print(f"Pitch shift is too high (expected ~6)")
            return False
    else:
        print(f"\n✗ FAILED: Could not estimate pitches")
        return False

if __name__ == "__main__":
    success = test_pitch_shift()
    sys.exit(0 if success else 1)
