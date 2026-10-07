import cv2
import numpy as np
import sys

from backend.multi_pin_bfs import detect_wire_colors_bfs


def base64_to_cv2_image(base64_str):
    if base64_str.startswith("data:image"):
        base64_str = base64_str.split(",", 1)[1]
    base64_str += "=" * (-len(base64_str) % 4)
    img_bytes = np.frombuffer(__import__("base64").b64decode(base64_str), np.uint8)
    return cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)


def _normalize_expected_count(expected_count):
    try:
        return int(expected_count)
    except (TypeError, ValueError):
        return None


def get_sequence_from_image(image, expected_count=None):
    """Public API for multi-pin wire detection.

    Args:
        image: BGR image array
        expected_count: approximate total wire count, e.g., 24

    Returns:
        (count, list_of_BGR_colors)
    """
    if image is None or image.size == 0:
        return 0, []

    expected_count = _normalize_expected_count(expected_count)
    count, colors = detect_wire_colors_bfs(image, expected_count)
    return count, colors


def get_double_sequence(front_image, back_image, expected_count=None):
    """Return front/back wire sequences."""
    if front_image is None or back_image is None:
        return (0, []), (0, [])

    f_count, f_colors = get_sequence_from_image(front_image, expected_count)
    b_count, b_colors = get_sequence_from_image(back_image, expected_count)
    return (f_count, f_colors), (b_count, b_colors)


def main():
    try:
        import json

        payload = json.loads(sys.stdin.read())
        images = payload.get("input", [])
        wire_type = payload.get("wireType")
        expected = payload.get("expected_count")

        if wire_type == "singlewire":
            img = base64_to_cv2_image(images[0])
            result = get_sequence_from_image(img, expected)
            print(json.dumps({"type": "singlewire", "sequence": result[1]}))
        elif wire_type == "doublewire":
            front = base64_to_cv2_image(images[0])
            back = base64_to_cv2_image(images[1])
            front_result, back_result = get_double_sequence(front, back, expected)
            print(json.dumps({
                "type": "doublewire",
                "sequence_front": front_result[1],
                "sequence_back": back_result[1],
            }))
        else:
            raise ValueError("Invalid wire type")
    except Exception as exc:  # pragma: no cover
        print(str(exc), file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
