import colorsys

_global_color_offset = 2
_local_color_offset = 0


def y_to_color(y: float) -> tuple[float, float, float]:
    return colorsys.hsv_to_rgb(((y + _global_color_offset + _local_color_offset) / 15.0) % 1, 1.0, 1.0)


def get_global_color_offset() -> float:
    return _global_color_offset


def set_global_color_offset(offset: float) -> None:
    global _global_color_offset
    _global_color_offset = offset


def get_local_color_offset() -> float:
    return _local_color_offset


def set_local_color_offset(offset: float) -> None:
    global _local_color_offset
    _local_color_offset = offset


def clamp(f: float, small: float, large: float) -> float:
    return max(small, min(f, large))
