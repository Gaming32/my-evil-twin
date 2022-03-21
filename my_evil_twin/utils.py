import colorsys


def y_to_color(y: float) -> tuple[float, float, float]:
    return colorsys.hsv_to_rgb((y / 15.0) % 1, 1.0, 1.0)
