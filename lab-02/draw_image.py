"""Створення абстрактної композиції примітивами OpenCV."""

from pathlib import Path

import cv2
import numpy as np


WIDTH = 525
HEIGHT = 549


def draw_image() -> np.ndarray:
    """Створює абстрактну композицію з трикутним силуетом і білими дугами."""
    image = np.full((HEIGHT, WIDTH, 3), 255, dtype=np.uint8)
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Суцільний трикутник побудовано горизонтальними відрізками.
    top_y = 12
    bottom_y = 531
    center_x = WIDTH // 2
    for y in range(top_y, bottom_y + 1):
        fraction = (y - top_y) / (bottom_y - top_y)
        left_x = round(center_x * (1 - fraction))
        right_x = round(center_x + (WIDTH - center_x - 1) * fraction)
        cv2.line(image, (left_x, y), (right_x, y), black, 1)

    # Внутрішні світлі елементи утворено еліпсами.
    cv2.ellipse(image, (center_x, 395), (57, 80), 0, 0, 360, white, cv2.FILLED)
    cv2.ellipse(image, (center_x, 619), (311, 176), 0, 0, 360, white, cv2.FILLED)
    return image


def main() -> None:
    output = Path(__file__).with_name("abstract_composition.png")
    success, encoded = cv2.imencode(".png", draw_image())
    if not success:
        raise RuntimeError(f"Не вдалося зберегти файл {output}")
    encoded.tofile(output)
    print(f"Зображення збережено: {output}")


if __name__ == "__main__":
    main()
