# Wire Harness MultiPin Detection

This project is built for detecting soldered wire harnesses with 24 or more pins using computer vision and a BFS-based connected-component algorithm. It focuses on:

- segmenting the connector region and wire bundle
- detecting individual wires in a dense multi-pin harness
- estimating the wire color sequence from left to right
- handling front/back side detection for dual-sided connectors
- comparing detected colors against a reference sequence or stored wire type

## Key idea

The original single-band wire logic works well for a small number of wires, but dense connector bundles need a more robust approach:

1. isolate the connector and wire bundle ROI
2. convert image to HSV
3. build a mask for wire pixels using saturation and darkness thresholds
4. run BFS / connected-component analysis to group pixels into individual wire regions
5. compute each wire's average color from the center of its component
6. sort by x-position and return the left-to-right sequence

This approach is much more stable for soldered multi-pin harnesses than relying on a single horizontal scan line.

## Repository layout

```text
backend/
  multi_pin_bfs.py    BFS and connected-component wire detector
  getsequence.py      detection pipeline and sequence extraction
  reference.py        reference storage and color comparison logic
  compare.py          sequence comparison for front/back harnesses
  test_multipin.py    validation tests
examples/
  sample_harness_test.py  example usage on a real image
README.md
requirements.txt
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Quick usage

```python
from backend.getsequence import get_sequence_from_image

img = cv2.imread("path/to/harness.jpg")
count, colors = get_sequence_from_image(img, expected_count=24)
print("wire_count:", count)
print("colors:", colors)
```

You can also compare to a known reference:

```python
from backend.compare import compare_single, compare_double

# single side
result = compare_single((24, [(0, 0, 255), ...]), img)

# front/back
result = compare_double(((24, front_ref), (24, back_ref)), (front_img, back_img))
```

## Runtime notes

- Works best on clear, well-lit images of the wire bundle
- For very dense bundles, adjust the HSV thresholds and minimum component size
- For mirrored side detection, the code compares direct and reversed ordering

## License

MIT
