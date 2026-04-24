#!/usr/bin/env python3
"""Test 3: Voice Comparison (Ashley vs Standard)"""

import subprocess
import os
import sys

def generate_voice(text, voice_name, output_file):
    """Generate audio with specific voice using stdin."""
    cmd = [
        "kokoro-tts",
        "-",  # Read from stdin
        "--voice", voice_name,
        "-o", output_file
    ]

    try:
        result = subprocess.run(
            cmd,
            input=text,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0 and os.path.exists(output_file)
    except Exception:
        return False

def test_voice_comparison():
    print("=" * 60)
    print("TEST 3: Voice Comparison (Ashley vs Standard)")
    print("=" * 60)

    test_text = "The quick brown fox jumps over the lazy dog."
    voices = {
        "ashley_neuro": "Ashley (blended + pitched +6 semitones)",
        "af_sarah": "Sarah (baseline - plain)",
        "af_bella": "Bella (baseline - softer)"
    }

    print(f"\nTest text: {test_text}")
    print(f"\nGenerating {len(voices)} versions for comparison...\n")

    files_created = {}

    for voice_key, description in voices.items():
        output_file = f"compare_{voice_key}.wav"
        print(f"  Generating {voice_key}... ", end="", flush=True)

        if generate_voice(test_text, voice_key, output_file):
            file_size = os.path.getsize(output_file)
            files_created[voice_key] = (output_file, file_size)
            print(f"✓ ({file_size} bytes)")
        else:
            print(f"✗ FAILED")

    if not files_created:
        print(f"\n✗ FAILED: No audio files generated")
        return False

    print(f"\n✓ SUCCESS: Generated {len(files_created)} audio files")
    print(f"\nFiles created:")
    for voice_key, (filename, size) in files_created.items():
        print(f"  - {filename} ({size} bytes)")

    print(f"\nComparison Guide:")
    print(f"  1. Open each file in a media player (VLC, Windows Media Player, etc.)")
    print(f"  2. Listen to compare_ashley_neuro.wav first")
    print(f"  3. Then listen to compare_af_sarah.wav")
    print(f"\nWhat you should hear:")
    print(f"  ✓ ashley_neuro: Higher pitched, warmer tone, clearer")
    print(f"  ✓ af_sarah: Lower pitched baseline for comparison")
    print(f"  ✓ af_bella: Softer tone, used in blend")
    print(f"\nExpected pitch difference: ~25% higher in ashley_neuro")
    print(f"Semitone difference: ~+6 semitones")

    return True

if __name__ == "__main__":
    success = test_voice_comparison()
    sys.exit(0 if success else 1)
