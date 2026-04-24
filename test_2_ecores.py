#!/usr/bin/env python3
"""Test 2: E-core Affinity Verification"""

import os
import sys
import subprocess
import time
import psutil

def test_ecores():
    print("=" * 60)
    print("TEST 2: E-core Affinity Verification")
    print("=" * 60)

    print(f"\nSystem Information:")
    print(f"  Total logical cores: {psutil.cpu_count(logical=True)}")
    print(f"  Total physical cores: {psutil.cpu_count(logical=False)}")
    print(f"  Current process affinity: {sorted(psutil.Process(os.getpid()).cpu_affinity())}")

    print(f"\ni9-13900KS Layout (expected):")
    print(f"  P-cores (performance): 0-15")
    print(f"  E-cores (efficiency): 16-23")

    # Run kokoro-tts
    test_text = "Testing E-core affinity."
    output_file = "test_ecores.wav"

    print(f"\nRunning: kokoro-tts '{test_text}' --voice ashley_neuro -o {output_file}")

    cmd = [
        "kokoro-tts",
        test_text,
        "--voice", "ashley_neuro",
        "-o", output_file
    ]

    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Give it time to start
        time.sleep(1)

        # Check child process affinity
        try:
            parent = psutil.Process(proc.pid)
            children = parent.children(recursive=True)

            print(f"\nParent process {proc.pid}:")
            try:
                parent_affinity = parent.cpu_affinity()
                print(f"  Affinity: {sorted(parent_affinity)}")
            except psutil.NoSuchProcess:
                pass

            print(f"\nChild processes:")
            if children:
                for child in children:
                    try:
                        affinity = child.cpu_affinity()
                        print(f"  Process {child.pid}: {sorted(affinity)}")
                        if all(16 <= cpu <= 23 for cpu in affinity):
                            print(f"    ✓ Locked to E-cores (16-23)")
                        else:
                            print(f"    ✗ NOT locked to E-cores")
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
            else:
                print(f"  (No child processes found yet)")
        except Exception as e:
            print(f"  Could not inspect child processes: {e}")

        # Wait for completion
        proc.wait(timeout=30)

        if proc.returncode == 0 and os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"\n✓ SUCCESS: Audio generated")
            print(f"  File: {output_file}")
            print(f"  Size: {file_size} bytes")
            return True
        else:
            print(f"\n✗ FAILED: Process exit code {proc.returncode}")
            return False

    except subprocess.TimeoutExpired:
        proc.kill()
        print(f"\n✗ FAILED: Timeout")
        return False
    except FileNotFoundError:
        print(f"\n✗ FAILED: kokoro-tts not found")
        return False
    except Exception as e:
        print(f"\n✗ FAILED: {e}")
        return False

if __name__ == "__main__":
    try:
        import psutil
    except ImportError:
        print("ERROR: psutil not installed")
        print("Install: pip install psutil>=5.9.0")
        sys.exit(1)

    success = test_ecores()
    sys.exit(0 if success else 1)
