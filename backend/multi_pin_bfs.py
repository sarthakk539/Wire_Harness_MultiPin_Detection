import cv2
import numpy as np
from collections import deque


def _safe_bgr_sample(image, x_center, y_center, radius=3):
    """Sample a small patch around a wire center and return the average BGR."""
    h, w = image.shape[:2]
    x1 = max(0, x_center - radius)
    x2 = min(w - 1, x_center + radius)
    y1 = max(0, y_center - radius)
    y2 = min(h - 1, y_center + radius)

    if x1 >= x2 or y1 >= y2:
        return None

    patch = image[y1:y2 + 1, x1:x2 + 1]
    if patch.size == 0:
        return None

    return tuple(np.mean(patch, axis=(0, 1)).astype(np.uint8).tolist())


def _find_best_roi(image):
    """Return a cropped ROI covering the connector and upper wire bundle."""
    if image is None or image.size == 0:
        return image

    h, w = image.shape[:2]
    if h <= 0 or w <= 0:
        return image

    # Keep a generous upper section where bundles are usually visible.
    top = max(0, int(h * 0.05))
    bottom = min(h, int(h * 0.78))
    left = max(0, int(w * 0.05))
    right = min(w, int(w * 0.95))
    return image[top:bottom, left:right]


def _build_wire_mask(image):
    """Create a binary wire mask in HSV space.

    It keeps high-saturation colored wires and very dark wires, which are common
    in harness assemblies. The mask is cleaned with morphology to remove small noise.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # selected wire-like pixels
    mask = ((s > 35) | (v < 90)) & (v > 20)
    mask = mask.astype(np.uint8) * 255

    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    return mask


def _connected_wire_components(mask):
    """Find connected wire-like components in the mask using BFS."""
    h, w = mask.shape
    visited = np.zeros_like(mask, dtype=np.bool_)
    components = []

    for y in range(h):
        for x in range(w):
            if mask[y, x] == 0 or visited[y, x]:
                continue

            q = deque([(x, y)])
            visited[y, x] = True
            pixels = []

            while q:
                cx, cy = q.popleft()
                pixels.append((cx, cy))

                for nx, ny in [(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)]:
                    if 0 <= nx < w and 0 <= ny < h:
                        if mask[ny, nx] != 0 and not visited[ny, nx]:
                            visited[ny, nx] = True
                            q.append((nx, ny))

            if len(pixels) < 15:
                continue

            xs = [p[0] for p in pixels]
            ys = [p[1] for p in pixels]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)

            width = max_x - min_x + 1
            height = max_y - min_y + 1
            if width < 3 or height < 3:
                continue

            cx = (min_x + max_x) // 2
            cy = (min_y + max_y) // 2
            components.append({
                "center": (cx, cy),
                "bbox": (min_x, min_y, max_x, max_y),
                "pixels": pixels,
            })

    return components


def detect_wire_colors_bfs(image, expected_count=None):
    """Detect multi-pin wire colors using BFS over a wire mask.

    Returns a sorted left-to-right list of BGR tuples representing each wire color.
    """
    if image is None or image.size == 0:
        return 0, []

    roi = _find_best_roi(image)
    if roi is None or roi.size == 0:
        return 0, []

    mask = _build_wire_mask(roi)
    if mask is None or mask.size == 0:
        return 0, []

    components = _connected_wire_components(mask)
    if not components:
        return 0, []

    wire_samples = []
    for comp in components:
        cx, cy = comp["center"]
        sample = _safe_bgr_sample(roi, cx, cy, radius=4)
        if sample is not None:
            wire_samples.append({
                "x": cx,
                "color": tuple(sample),
            })

    if not wire_samples:
        return 0, []

    wire_samples.sort(key=lambda item: item["x"])

    if expected_count is not None and len(wire_samples) > expected_count:
        # choose left-most expected_count components by x-position
        wire_samples = wire_samples[:expected_count]

    colors = [entry["color"] for entry in wire_samples]
    return len(colors), colors


def detect_front_back_bfs(front_image, back_image, expected_count=None):
    """Return sequence for both front and back images."""
    front_count, front_colors = detect_wire_colors_bfs(front_image, expected_count)
    back_count, back_colors = detect_wire_colors_bfs(back_image, expected_count)
    return (front_count, front_colors), (back_count, back_colors)
