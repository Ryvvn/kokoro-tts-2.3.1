#!/usr/bin/env python3
"""CPU affinity management for Kokoro TTS on Intel i9-13900KS.

Handles locking Kokoro to E-cores (efficiency cores) for optimal power efficiency
on mixed-core CPUs. i9-13900KS has 8 P-cores (0-15) and 8 E-cores (16-23).
"""

import os
import sys

try:
    import psutil
except ImportError:
    psutil = None


def get_cpu_info():
    """Get info about CPU cores (P-cores vs E-cores)."""
    if psutil is None:
        return {"available": False, "reason": "psutil not installed"}

    try:
        # Get physical core count info
        phys_cores = psutil.cpu_count(logical=False)
        logical_cores = psutil.cpu_count(logical=True)

        return {
            "available": True,
            "physical_cores": phys_cores,
            "logical_cores": logical_cores,
        }
    except Exception as e:
        return {"available": False, "reason": str(e)}


def set_e_core_affinity(cpu_mask=None):
    """Lock current process to E-cores on i9-13900KS.

    Args:
        cpu_mask: Optional explicit CPU mask. Defaults to E-cores on i9-13900KS.
                 For i9-13900KS: E-cores are 16-23

    Returns:
        bool: True if affinity was set, False otherwise
    """
    if psutil is None:
        return False

    try:
        if cpu_mask is None:
            cpu_mask = list(range(16, 32))  # E-cores: 16-23 on i9-13900KS

        process = psutil.Process(os.getpid())
        process.cpu_affinity(cpu_mask)      
        return True
    except Exception:
        return False


def set_p_core_affinity():
    """Lock current process to P-cores on i9-13900KS."""
    if psutil is None:
        return False

    try:
        cpu_mask = list(range(0, 16))  # P-cores: 0-15 on i9-13900KS
        process = psutil.Process(os.getpid())
        process.cpu_affinity(cpu_mask)
        return True
    except Exception:
        return False


def get_current_affinity():
    """Get current process CPU affinity."""
    if psutil is None:
        return None

    try:
        process = psutil.Process(os.getpid())
        return sorted(process.cpu_affinity())
    except Exception:
        return None


def reset_affinity():
    """Reset CPU affinity to all available cores."""
    if psutil is None:
        return False

    try:
        info = get_cpu_info()
        if not info["available"]:
            return False

        cpu_mask = list(range(info["logical_cores"]))
        process = psutil.Process(os.getpid())
        process.cpu_affinity(cpu_mask)
        return True
    except Exception:
        return False


if __name__ == "__main__":
    # Test script
    print("CPU Affinity Information:")
    info = get_cpu_info()
    if info["available"]:
        print(f"  Physical cores: {info['physical_cores']}")
        print(f"  Logical cores: {info['logical_cores']}")
    else:
        print(f"  Not available: {info['reason']}")

    print("\nCurrent affinity:", get_current_affinity())

    print("\nSetting E-core affinity...")
    if set_e_core_affinity():
        print("  ✓ E-core affinity set")
        print(f"  Current affinity: {get_current_affinity()}")
    else:
        print("  ✗ Failed to set E-core affinity")
