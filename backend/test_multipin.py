import cv2
import numpy as np

from backend.multi_pin_bfs import detect_wire_colors_bfs


def test_detect_wire_colors_bfs_handles_dense_bundle():
    h, w = 400, 800
    img = np.zeros((h, w, 3), dtype=np.uint8)

    # Create a few colored wire-like vertical bands.
    for x_index, color in enumerate([
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255),
    ]):
        x_start = 120 + x_index * 130
        cv2.rectangle(img, (x_start, 80), (x_start + 14, 260), color, -1)

    count, colors = detect_wire_colors_bfs(img, expected_count=5)
    assert count == 5
    assert len(colors) == 5


def test_detect_wire_colors_bfs_returns_zero_for_empty_image():
    img = np.zeros((50, 50, 3), dtype=np.uint8)
    count, colors = detect_wire_colors_bfs(img, expected_count=5)
    assert count == 0
    assert colors == []


def test_detect_wire_colors_bfs_handles_black_wire():
    img = np.zeros((250, 500, 3), dtype=np.uint8)
    cv2.rectangle(img, (100, 30), (130, 180), (0, 0, 0), -1)
    cv2.rectangle(img, (220, 30), (250, 180), (10, 10, 10), -1)

    count, colors = detect_wire_colors_bfs(img, expected_count=2)
    assert count >= 1
    assert len(colors) >= 1
