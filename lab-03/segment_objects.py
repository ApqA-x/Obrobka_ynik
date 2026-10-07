"""Сегментація кольорових об'єктів на світлому тлі та їх підрахунок."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def segment_objects(image: np.ndarray) -> tuple[np.ndarray, int]:
    """Повертає маску червоних об'єктів та їх кількість."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Червоний колір міститься на початку та в кінці шкали відтінку HSV.
    lower_red = cv2.inRange(hsv, (0, 60, 50), (8, 255, 255))
    upper_red = cv2.inRange(hsv, (170, 60, 50), (179, 255, 255))
    mask = cv2.bitwise_or(lower_red, upper_red)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=3)

    count, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    cleaned = np.zeros_like(mask)
    objects = 0
    # Площа відсікає дрібні червоні відблиски та шум.
    min_area = image.shape[0] * image.shape[1] * 0.003

    for label in range(1, count):
        if stats[label, cv2.CC_STAT_AREA] >= min_area:
            cleaned[labels == label] = 255
            objects += 1

    return cleaned, objects


def read_image(path: Path) -> np.ndarray | None:
    """Зчитує зображення зі шляху, який може містити українські літери."""
    encoded = np.fromfile(path, dtype=np.uint8)
    return cv2.imdecode(encoded, cv2.IMREAD_COLOR)


def write_image(path: Path, image: np.ndarray) -> bool:
    """Зберігає зображення за шляхом, який може містити українські літери."""
    success, encoded = cv2.imencode(path.suffix, image)
    if success:
        encoded.tofile(path)
    return success


def create_result(image: np.ndarray, mask: np.ndarray, objects: int) -> np.ndarray:
    """Створює зображення з контурами й підписом кількості об'єктів."""
    result = image.copy()
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for number, contour in enumerate(contours, start=1):
        x, y, w, h = cv2.boundingRect(contour)
        cv2.drawContours(result, [contour], -1, (0, 0, 255), 4)
        cv2.putText(result, str(number), (x, max(y - 12, 30)), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3, cv2.LINE_AA)
    # Шрифт Pillow підтримує українські літери, на відміну від базового шрифту OpenCV.
    rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    canvas = Image.fromarray(rgb)
    drawer = ImageDraw.Draw(canvas)
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 34)
    drawer.text((25, 15), f"Кількість об'єктів: {objects}", font=font, fill=(255, 0, 0), stroke_width=1, stroke_fill=(255, 255, 255))
    return cv2.cvtColor(np.array(canvas), cv2.COLOR_RGB2BGR)


def main() -> None:
    parser = argparse.ArgumentParser(description="Сегментація кольорових об'єктів.")
    parser.add_argument("image", type=Path, help="Шлях до вхідного зображення")
    parser.add_argument("--output", type=Path, default=Path("result.png"), help="Шлях до зображення-результату")
    args = parser.parse_args()

    image = read_image(args.image)
    if image is None:
        raise FileNotFoundError(f"Не вдалося прочитати зображення: {args.image}")

    mask, objects = segment_objects(image)
    result = create_result(image, mask, objects)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if not write_image(args.output, result):
        raise RuntimeError(f"Не вдалося зберегти результат: {args.output}")
    print(f"Кількість об'єктів: {objects}")
    print(f"Результат збережено: {args.output}")


if __name__ == "__main__":
    main()
