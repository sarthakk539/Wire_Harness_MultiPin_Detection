#!/usr/bin/env python3
"""
Build Python wheel package.

Usage:
  python build_wheel.py

This creates a .whl file that can be installed with pip.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def check_build_tools():
    """Check if build tools are installed."""
    try:
        import wheel
        import build
        return True
    except ImportError:
        print("Build tools not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "wheel", "build"])
        return True


def build_wheel():
    """Build wheel package."""
    print("\n" + "=" * 80)
    print("Building Wire Harness Detector Wheel Package")
    print("=" * 80 + "\n")

    if not check_build_tools():
        print("ERROR: Failed to install build tools")
        return False

    # Clean previous builds
    if os.path.exists("dist"):
        print("Cleaning previous builds...")
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")

    print("Building wheel...")
    try:
        subprocess.check_call([sys.executable, "-m", "build"])
        print("\n" + "=" * 80)
        print("✓ Build successful!")
        print("=" * 80)
        print(f"\nWheel package location: {os.path.join('dist')}")
        print(f"\nInstall with:")
        print(f"  pip install dist/wire_harness_detector-1.0.0-py3-none-any.whl")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: Build failed: {e}")
        return False


if __name__ == "__main__":
    success = build_wheel()
    sys.exit(0 if success else 1)
