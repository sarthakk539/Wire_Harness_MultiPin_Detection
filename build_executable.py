#!/usr/bin/env python3
"""
Build executable using PyInstaller.

Usage:
  python build_executable.py

This creates a standalone executable that doesn't require Python to be installed.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def check_pyinstaller():
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller
        return True
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return True


def build_executable():
    """Build standalone executable."""
    print("\n" + "=" * 80)
    print("Building Wire Harness Detector Executable")
    print("=" * 80 + "\n")

    if not check_pyinstaller():
        print("ERROR: Failed to install PyInstaller")
        return False

    # Clean previous builds
    if os.path.exists("dist"):
        print("Removing previous build...")
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("wire_harness_detector.spec"):
        os.remove("wire_harness_detector.spec")

    print("Building executable...")
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed" if sys.platform == "win32" else "",
        "--icon=assets/icon.ico" if os.path.exists("assets/icon.ico") else "",
        "--add-data",
        "backend:backend",
        "--name",
        "WireHarnessDetector",
        "app.py",
    ]
    # Remove empty strings
    cmd = [arg for arg in cmd if arg]

    try:
        subprocess.check_call(cmd)
        print("\n" + "=" * 80)
        print("✓ Build successful!")
        print("=" * 80)
        print(f"\nExecutable location: {os.path.join('dist', 'WireHarnessDetector')}")
        if sys.platform == "win32":
            print(f"Run: dist\\WireHarnessDetector.exe")
        else:
            print(f"Run: ./dist/WireHarnessDetector")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: Build failed: {e}")
        return False


if __name__ == "__main__":
    success = build_executable()
    sys.exit(0 if success else 1)
