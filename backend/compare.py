import json
import sys

import cv2
import numpy as np

from backend.getsequence import get_sequence_from_image
from backend.reference import _wire_color_distance, _classify_hue, _bgr_to_hsv_components


def base64_to_cv2_image(base64_list):
    images = []
    for base64_str in base64_list:
        if base64_str.startswith("data:image"):
            base64_str = base64_str.split(",", 1)[1]
        base64_str += "=" * (-len(base64_str) % 4)
        decoded = __import__("base64").b64decode(base64_str)
        np_data = np.frombuffer(decoded, np.uint8)
        img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        images.append(img)
    return images


def compare_single(original, input_image, hue_threshold=130):
    desired_num_wires, desired_colors = original[0], original[1]
    _, detected_colors = get_sequence_from_image(input_image, expected_count=desired_num_wires)

    if len(detected_colors) != desired_num_wires:
        return {
            "match": False,
            "details": f"Expected {desired_num_wires} wires, detected {len(detected_colors)}",
        }

    mismatches = []
    for i, (desired_bgr, detected_bgr) in enumerate(zip(desired_colors, detected_colors)):
        dist = _wire_color_distance(tuple(desired_bgr), tuple(detected_bgr))
        if dist > hue_threshold:
            desired_name = _classify_hue(*_bgr_to_hsv_components(tuple(desired_bgr)))
            detected_name = _classify_hue(*_bgr_to_hsv_components(tuple(detected_bgr)))
            mismatches.append(
                f"Wire {i + 1}: expected {desired_name}, got {detected_name} [dist={dist:.1f}]"
            )

    if not mismatches:
        return {"match": True, "details": "SUCCESSFUL: Number of wires and colors match."}
    return {"match": False, "details": "; ".join(mismatches)}


def compare_double(original, input_image, hue_threshold=130):
    desired_front_num, desired_front_colors = original[0][0], original[0][1]
    desired_back_num, desired_back_colors = original[1][0], original[1][1]
    front_image, back_image = input_image

    _, detected_front_colors = get_sequence_from_image(front_image, expected_count=desired_front_num)
    _, detected_back_colors = get_sequence_from_image(back_image, expected_count=desired_back_num)

    mismatches = []

    def _compare_side(label, desired_num, desired_colors, detected_colors):
        if len(detected_colors) != desired_num:
            mismatches.append(f"{label}: expected {desired_num} wires, detected {len(detected_colors)}")
            return

        side_mismatches = []
        for i, (des_bgr, det_bgr) in enumerate(zip(desired_colors, detected_colors)):
            dist = _wire_color_distance(tuple(des_bgr), tuple(det_bgr))
            if dist > hue_threshold:
                des_name = _classify_hue(*_bgr_to_hsv_components(tuple(des_bgr)))
                det_name = _classify_hue(*_bgr_to_hsv_components(tuple(det_bgr)))
                side_mismatches.append(
                    f"Wire {i + 1}: expected {des_name}, got {det_name} [dist={dist:.1f}]"
                )

        if side_mismatches:
            mismatches.append(f"{label}: {'; '.join(side_mismatches)}")

    _compare_side("Front", desired_front_num, desired_front_colors, detected_front_colors)
    _compare_side("Back", desired_back_num, desired_back_colors, detected_back_colors)

    if not mismatches:
        return {"match": True, "details": "SUCCESSFUL: Both front and back sequences match."}
    return {"match": False, "details": " | ".join(mismatches)}


def main():
    try:
        raw_input = sys.stdin.read()
        data = json.loads(raw_input)
        wire_count = data["wire_count"]
        sequence = data["sequence"]
        stringified_rgb_list = json.loads(sequence)
        sequence = [json.loads(rgb) for rgb in stringified_rgb_list]
        test_images = base64_to_cv2_image(data["input"])
        wire_type = data["wireType"]

        if wire_type == "singlewire":
            result = compare_single([wire_count[0], sequence[0]], test_images[0])
        elif wire_type == "doublewire":
            result = compare_double(
                [[wire_count[0], sequence[0]], [wire_count[1], sequence[1]]],
                test_images,
            )
        else:
            raise ValueError("Invalid wire type")

        print(json.dumps(result))
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
