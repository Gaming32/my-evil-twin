import colorsys

_color_offset = 0


def y_to_color(y: float) -> tuple[float, float, float]:
    return colorsys.hsv_to_rgb(((y + _color_offset) / 15.0) % 1, 1.0, 1.0)


def set_color_offset(offset: float) -> None:
    global _color_offset
    _color_offset = offset
