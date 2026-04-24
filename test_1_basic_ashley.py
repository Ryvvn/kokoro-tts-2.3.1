#!/usr/bin/env python3
"""Test 1: Basic Ashley Voice Output"""

import subprocess
import os
import sys

def test_ashley_basic():
    print("=" * 60)
    print("TEST 1: Basic Ashley Voice Output")
    print("=" * 60)

    test_text = "Hello, I'm Ashley. This is the neuro vtuber voice."
    output_file = "ashley_test.wav"

    print(f"\nTest text: {test_text}")
    print(f"Output file: {output_file}")
    print("\nGenerating audio...")

    # Use stdin to pass text (correct Kokoro usage)
    cmd = [
        "kokoro-tts",
        "-",  # Read from stdin
        "--voice", "ashley_neuro",
        "-o", output_file
    ]

    try:
        result = subprocess.run(
            cmd,
            input=test_text,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                print(f"\n✓ SUCCESS: Audio file created")
                print(f"  File: {output_file}")
                print(f"  Size: {file_size} bytes")
                print(f"\nExpected characteristics:")
                print(f"  - Warm, clear female voice")
                print(f"  - Noticeably higher pitch (~25% up)")
                print(f"  - Blend of af_sarah (70%) + af_bella (30%)")
                return True
            else:
                print(f"\n✗ FAILED: File not created despite success exit code")
                return False
        else:
            print(f"\n✗ FAILED: Command exited with code {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr}")
            if result.stdout:
                print(f"Output: {result.stdout}")
            return False

    except subprocess.TimeoutExpired:
        print(f"\n✗ FAILED: Command timed out after 30 seconds")
        return False
    except FileNotFoundError:
        print(f"\n✗ FAILED: kokoro-tts command not found")
        print(f"Install it: pip install -e d:\\AICompanionProject\\kokoro-tts-2.3.1")
        return False
    except Exception as e:
        print(f"\n✗ FAILED: {e}")
        return False

if __name__ == "__main__":
    success = test_ashley_basic()
    sys.exit(0 if success else 1)
