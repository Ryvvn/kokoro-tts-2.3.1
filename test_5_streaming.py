#!/usr/bin/env python3
"""Test 5: Streaming Mode"""

import subprocess
import sys
import os

def test_streaming():
    print("=" * 60)
    print("TEST 5: Streaming Mode (Real-time Playback)")
    print("=" * 60)

    # Create longer test text
    test_text = """Hello, I'm Ashley, your AI vtuber voice. I can speak naturally with
pitch and warmth. Testing the streaming capability to see latency and quality.
This demonstrates real-time speech synthesis with E-core optimization on
your i9-13900KS CPU. The streaming mode should show minimal latency between
chunks and smooth playback of longer content."""

    print(f"\nTest text ({len(test_text)} characters):")
    print(f"  {test_text[:80]}...")

    print(f"\nRunning: echo text | kokoro-tts - --voice ashley_neuro --stream")
    print(f"Expected behavior:")
    print(f"  - Audio starts after ~1-2 seconds (first chunk)")
    print(f"  - Continuous playback with minimal gaps")
    print(f"  - Process completes without errors")

    cmd = [
        "kokoro-tts",
        "-",  # Read from stdin
        "--voice", "ashley_neuro",
        "--stream"
    ]

    try:
        print(f"\nStarting stream...\n")
        result = subprocess.run(
            cmd,
            input=test_text,
            capture_output=False,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            print(f"\n✓ SUCCESS: Streaming completed without errors")
            return True
        else:
            print(f"\n✗ FAILED: Process exited with code {result.returncode}")
            return False

    except subprocess.TimeoutExpired:
        print(f"\n✗ FAILED: Streaming timed out after 60 seconds")
        return False
    except FileNotFoundError:
        print(f"\n✗ FAILED: kokoro-tts command not found")
        return False
    except Exception as e:
        print(f"\n✗ FAILED: {e}")
        return False

if __name__ == "__main__":
    print("WARNING: This test will play audio. Make sure speakers are connected.\n")

    success = test_streaming()
    sys.exit(0 if success else 1)
