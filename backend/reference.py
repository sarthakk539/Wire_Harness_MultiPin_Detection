import json
import os

import cv2
import numpy as np

from backend.getsequence import get_sequence_from_image


def _hue_angle_diff(h1_deg, h2_deg):
    diff = abs(h1_deg - h2_deg) % 360
    return diff if diff <= 180 else 360 - diff


def _bgr_to_hsv_components(bgr_tuple):
    pixel = np.array([[list(bgr_tuple)]], dtype=np.uint8)
    hsv = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)[0][0]
    h_deg = int(hsv[0]) * 2
    s = int(hsv[1])
    v = int(hsv[2])
    return h_deg, s, v


def _classify_hue(h_deg, s, v):
    if v < 60:
        return "black"
    if s < 45:
        return "white" if v > 200 else "gray"
    if h_deg <= 20 and s > 60 and v < 150:
        return "brown"
    if h_deg <= 12 or h_deg >= 348:
        return "red"
    if h_deg <= 30:
        return "orange"
    if h_deg <= 70:
        return "yellow"
    if h_deg <= 160:
        return "green"
    if h_deg <= 200:
        return "cyan"
    if h_deg <= 260:
        return "blue"
    if h_deg <= 320:
        return "purple"
    if h_deg <= 348:
        return "pink"
    return "red"


def _wire_color_distance(bgr_a, bgr_b):
    h1, s1, v1 = _bgr_to_hsv_components(bgr_a)
    h2, s2, v2 = _bgr_to_hsv_components(bgr_b)

    if v1 < 60 and v2 < 60:
        return abs(v1 - v2)
    if v1 < 60 or v2 < 60:
        return 180.0

    if s1 < 40 and s2 < 40:
        return abs(v1 - v2) * 0.5
    if s1 < 40 or s2 < 40:
        return 90.0

    hue_diff = _hue_angle_diff(h1, h2)
    sat_diff = abs(s1 - s2) / 255.0 * 30
    val_diff = abs(v1 - v2) / 255.0 * 20
    return hue_diff + sat_diff + val_diff


def store_reference(image, num_wires, save_path="reference.json"):
    count, colors = get_sequence_from_image(image, expected_count=num_wires)
    data = {
        "num_wires": num_wires,
        "color_sequence": [list(c) for c in colors],
        "color_names": [_classify_hue(*_bgr_to_hsv_components(c)) for c in colors],
    }

    with open(save_path, "w") as f:
        json.dump(data, f, indent=2)

    return count, colors


def verify_against_reference(new_image, reference_path="reference.json", hue_threshold=130):
    if not os.path.exists(reference_path):
        return {"match": False, "details": "Reference file not found", "wire_comparisons": []}

    with open(reference_path) as f:
        ref = json.load(f)

    num_wires = ref["num_wires"]
    ref_colors = [tuple(c) for c in ref["color_sequence"]]
    _, new_colors = get_sequence_from_image(new_image, expected_count=num_wires)

    if len(new_colors) < num_wires // 2:
        return {"match": False, "details": "Too few wires detected", "wire_comparisons": []}

    comparisons = []
    for i in range(min(len(ref_colors), len(new_colors))):
        ref_color = ref_colors[i]
        det_color = new_colors[i]
        dist = _wire_color_distance(ref_color, det_color)
        comparisons.append({
            "wire": i + 1,
            "match": dist <= hue_threshold,
            "distance": round(dist, 2),
            "reference_bgr": list(ref_color),
            "detected_bgr": list(det_color),
        })

    ok = all(item["match"] for item in comparisons) if comparisons else False
    return {"match": ok, "details": "reference verification", "wire_comparisons": comparisons}
