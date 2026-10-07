import cv2
import numpy as np

from backend.getsequence import get_sequence_from_image


def demo():
    img = np.zeros((500, 900, 3), dtype=np.uint8)
    colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255),
        (0, 255, 255),
    ]

    for i, color in enumerate(colors):
        x = 80 + i * 120
        cv2.rectangle(img, (x, 80), (x + 20, 260), color, -1)

    count, result = get_sequence_from_image(img, expected_count=len(colors))
    print(f"Detected wires: {count}")
    print(result)


if __name__ == "__main__":
    demo()
