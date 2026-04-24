#!/usr/bin/env python3
"""Master Test Suite - Run all tests sequentially"""

import subprocess
import sys
import os

TESTS = [
    ("test_1_basic_ashley.py", "Basic Ashley Voice Output"),
    ("test_2_ecores.py", "E-core Affinity Verification"),
    ("test_3_voice_comparison.py", "Voice Comparison"),
    ("test_4_cpu_affinity.py", "CPU Affinity Module"),
    ("test_5_streaming.py", "Streaming Mode"),
    ("test_6_pitch_shift.py", "Pitch Shift Verification"),
]

def run_test(script_name, description):
    """Run a single test script."""
    print("\n")
    print("=" * 70)
    print(f"Running: {description}")
    print("=" * 70)

    if not os.path.exists(script_name):
        print(f"✗ SKIPPED: {script_name} not found")
        return None

    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=False,
            timeout=120
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"✗ TIMEOUT: Test took too long")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False

def main():
    print("=" * 70)
    print("ASHLEY VOICE - COMPLETE TEST SUITE")
    print("=" * 70)
    print("\nThis will run all 6 tests to verify Ashley voice implementation.")
    print("Some tests require audio files from previous tests.")
    print("\nRecommended run order:")
    for i, (_, desc) in enumerate(TESTS, 1):
        print(f"  {i}. {desc}")

    input("\nPress Enter to start, or Ctrl+C to cancel...")

    results = {}

    for script_name, description in TESTS:
        result = run_test(script_name, description)
        results[description] = result

    # Summary
    print("\n")
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for r in results.values() if r is True)
    failed = sum(1 for r in results.values() if r is False)
    skipped = sum(1 for r in results.values() if r is None)

    for description, result in results.items():
        status = "✓ PASS" if result is True else "✗ FAIL" if result is False else "⊘ SKIP"
        print(f"{status:8} {description}")

    print("\n" + "-" * 70)
    print(f"Results: {passed} passed, {failed} failed, {skipped} skipped")

    if failed == 0 and passed > 0:
        print("\n✓ ALL TESTS PASSED!")
        print("Ashley voice is ready to use:")
        print("  kokoro-tts 'Hello, I'm Ashley.' --voice ashley_neuro")
        return 0
    elif failed > 0:
        print(f"\n✗ {failed} test(s) failed. Check output above for details.")
        return 1
    else:
        print("\n⚠ No tests were run successfully.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
