# BFS-based wire detection algorithm

The detector works in a sequence:

1. Crop the connector and upper bundle region.
2. Convert to HSV.
3. Keep pixels with enough saturation or a dark value.
4. Build a binary mask and clean it with morphology.
5. Run BFS connected-component analysis to isolate each wire region.
6. Sample the center color per component.
7. Sort all detected centers by x-coordinate.
8. Return the wire sequence left-to-right.

This is more reliable than a single horizontal line scan for dense 24+ pin harnesses.

## Why BFS matters

In a crowded connector image, wires share adjacent pixels and often appear as continuous clusters. A BFS pass groups connected pixels into one connected object, which makes it easier to estimate the wire center and color even when wires are packed tightly.

## Front and back handling

For front/back connectors, the detector can run independently on both images. If they are mirror images, the comparison should evaluate both direct and reversed order.

## Main functions

- `backend.multi_pin_bfs.detect_wire_colors_bfs(image, expected_count=None)`
- `backend.getsequence.get_sequence_from_image(image, expected_count=None)`
- `backend.compare.compare_single(original, input_image, hue_threshold=130)`
- `backend.compare.compare_double(original, input_image, hue_threshold=130)`
