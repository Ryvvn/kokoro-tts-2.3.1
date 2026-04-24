#!/usr/bin/env python3
"""Test 4: CPU Affinity Module Direct Test"""

import sys
import os

def test_cpu_affinity_module():
    print("=" * 60)
    print("TEST 4: CPU Affinity Module Direct Test")
    print("=" * 60)

    try:
        import psutil
        print("\n✓ psutil installed")
    except ImportError:
        print("\n✗ FAILED: psutil not installed")
        print("  Install: pip install psutil>=5.9.0")
        return False

    try:
        from kokoro_tts.cpu_affinity import (
            get_cpu_info,
            set_e_core_affinity,
            get_current_affinity,
            reset_affinity
        )
        print("✓ cpu_affinity module imported")
    except ImportError as e:
        print(f"\n✗ FAILED: Could not import cpu_affinity module")
        print(f"  Error: {e}")
        return False

    # Test get_cpu_info
    print("\n--- CPU Information ---")
    info = get_cpu_info()
    if info["available"]:
        print(f"✓ CPU info available")
        print(f"  Physical cores: {info['physical_cores']}")
        print(f"  Logical cores: {info['logical_cores']}")
    else:
        print(f"✗ CPU info not available: {info['reason']}")
        return False

    # Test get current affinity
    print("\n--- Current Affinity ---")
    current = get_current_affinity()
    if current:
        print(f"✓ Current affinity: {current}")
    else:
        print(f"✗ Could not get current affinity")
        return False

    # Test set E-core affinity
    print("\n--- Setting E-core Affinity ---")
    result = set_e_core_affinity()
    if result:
        print(f"✓ E-core affinity set successfully")
        new_affinity = get_current_affinity()
        print(f"  New affinity: {new_affinity}")

        # Verify it's actually set to E-cores (16-23)
        expected_ecores = list(range(16, 24))
        if new_affinity == expected_ecores:
            print(f"  ✓ Correctly locked to E-cores (16-23)")
            return True
        else:
            print(f"  ✗ Affinity not E-cores")
            print(f"    Expected: {expected_ecores}")
            print(f"    Got: {new_affinity}")
            return False
    else:
        print(f"✗ Failed to set E-core affinity")
        return False

if __name__ == "__main__":
    success = test_cpu_affinity_module()
    if success:
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED: CPU affinity module works!")
        print("=" * 60)
    sys.exit(0 if success else 1)
