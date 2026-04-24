#!/usr/bin/env python3
"""Quick test of Ashley voice fix"""

import subprocess
import sys

print("Testing Ashley voice with debug...")
print("=" * 60)

text = "Hello I am Ashley."

cmd = [
    sys.executable, "-m", "kokoro_tts",
    "-",  # stdin
    "--voice", "ashley_neuro",
    "--debug",
    "-o", "ashley_test_fix.wav"
]

result = subprocess.run(
    cmd,
    input=text,
    text=True,
    cwd="/d/AICompanionProject/kokoro-tts-2.3.1"
)

print("\n" + "=" * 60)
if result.returncode == 0:
    print("✓ SUCCESS - ashley_test_fix.wav created!")
else:
    print("✗ Failed with exit code:", result.returncode)

sys.exit(result.returncode)
