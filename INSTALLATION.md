# Installation & Executable Package Guide

## Option 1: Standalone Executable (Recommended for End Users)

No Python installation required. Just download and run.

### Windows

1. **Download** `WireHarnessDetector.exe` from releases
2. **Run** the executable
3. **Use** via command line:
   ```cmd
   WireHarnessDetector.exe detect --image harness.jpg --expected 24
   ```

### macOS / Linux

1. **Download** `WireHarnessDetector` from releases
2. **Make executable**:
   ```bash
   chmod +x WireHarnessDetector
   ```
3. **Run**:
   ```bash
   ./WireHarnessDetector detect --image harness.jpg --expected 24
   ```

### Build Executable Yourself

If you want to build from source:

```bash
git clone https://github.com/sarthakk539/Wire_Harness_MultiPin_Detection.git
cd Wire_Harness_MultiPin_Detection

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build executable
python build_executable.py

# Output will be in dist/ folder
```

---

## Option 2: Python Package (pip install)

For developers or users with Python installed.

### Install from PyPI (when available)

```bash
pip install wire-harness-detector
wire-harness detect --image harness.jpg --expected 24
```

### Install from GitHub

```bash
pip install git+https://github.com/sarthakk539/Wire_Harness_MultiPin_Detection.git
```

### Build Wheel Yourself

```bash
git clone https://github.com/sarthakk539/Wire_Harness_MultiPin_Detection.git
cd Wire_Harness_MultiPin_Detection

pip install -r requirements.txt
pip install build wheel

python build_wheel.py

# Install the wheel
pip install dist/wire_harness_detector-1.0.0-py3-none-any.whl
```

---

## Option 3: Docker Container

Isolated environment with all dependencies included.

### Build Docker Image

```bash
git clone https://github.com/sarthakk539/Wire_Harness_MultiPin_Detection.git
cd Wire_Harness_MultiPin_Detection

docker build -t wire-harness-detector:latest .
```

### Run Docker Container

```bash
docker run --rm -v $(pwd):/data wire-harness-detector:latest \
  detect --image /data/harness.jpg --expected 24
```

---

## Option 4: Development Setup

For contributors or development work.

```bash
git clone https://github.com/sarthakk539/Wire_Harness_MultiPin_Detection.git
cd Wire_Harness_MultiPin_Detection

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
pip install -e .

python app.py --help
```

---

## Verification

Test your installation:

```bash
# Single-side detection
wire-harness detect --image test_image.jpg --expected 24

# Dual-side detection
wire-harness detect-dual --front front.jpg --back back.jpg --expected 24

# Store reference
wire-harness reference --image ref.jpg --num-wires 24 --output reference.json

# Verify against reference
wire-harness verify --image test.jpg --reference reference.json
```

---

## Troubleshooting

### "Command not found: wire-harness"

**Solution:** Reinstall the package:
```bash
pip install --force-reinstall wire-harness-detector
```

### "No module named cv2"

**Solution:** OpenCV not installed properly:
```bash
pip install --upgrade opencv-python
```

### "Image file not found"

**Solution:** Use absolute path or check file exists:
```bash
# Use full path
wire-harness detect --image /full/path/to/image.jpg

# Check file
ls -la /path/to/image.jpg
```

### Executable crashes on startup (Windows)

**Solution:** Install Visual C++ Redistributable:
- Download from: https://support.microsoft.com/en-us/help/2977003
- Install the latest x64 or x86 version matching your system

### Slow performance on first run

**Normal behavior:** First execution loads OpenCV libraries (~2-5 seconds).

---

## Quick Start Examples

### Example 1: Detect wires in a single image

```bash
wire-harness detect --image harness_connector.jpg --expected 24
```

**Output:**
- Console: Wire count and colors
- Log file: `logs/detection_YYYYMMDD_HHMMSS.log`

### Example 2: Compare front and back

```bash
wire-harness detect-dual --front connector_front.jpg --back connector_back.jpg --expected 24
```

### Example 3: Store reference for quality control

```bash
# Store a known-good harness as reference
wire-harness reference --image good_harness.jpg --num-wires 24 --output good_harness_ref.json

# Later, verify new harnesses
wire-harness verify --image test_harness.jpg --reference good_harness_ref.json
```

### Example 4: Batch processing

```bash
python examples/batch_processor.py /path/to/images/ --count 24 --output report.json
```

---

## System Requirements

### Minimum (Executable)
- Windows 10+ / macOS 10.13+ / Linux (Ubuntu 18.04+)
- 200 MB disk space
- 2 GB RAM

### Recommended (Executable)
- Windows 10+ / macOS 11+ / Linux (Ubuntu 20.04+)
- 500 MB disk space
- 4 GB RAM

### Development (Python)
- Python 3.8+
- pip package manager
- 1 GB disk space for dependencies

---

## Support

For issues or questions:
1. Check the logs: `logs/detection_*.log`
2. Read docs: https://github.com/sarthakk539/Wire_Harness_MultiPin_Detection/tree/main/docs
3. Open an issue: https://github.com/sarthakk539/Wire_Harness_MultiPin_Detection/issues
