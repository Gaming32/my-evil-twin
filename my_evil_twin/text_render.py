# Huge credit to Notch for creating this text renderer for Minecraft

import random
from importlib import resources

import numpy as np
import PIL.Image
from OpenGL.GL import *
from pygame.color import Color

import my_evil_twin

CHAR_WIDTH: list[int] = []

with resources.open_binary(my_evil_twin, 'default_font.png') as _fp:
    _font_image = PIL.Image.open(_fp).convert('RGBA')
_fi_width = _font_image.width
_fi_height = _font_image.height
_pixel_data = [
    # (c[0] << 24) | (c[1] << 16) | (c[2] << 8) | c[3]
    (c[3] << 24) | (c[0] << 16) | (c[1] << 8) | c[2]
    for c in np.asarray(_font_image, np.int32).reshape(_fi_width * _fi_height, 4)
]
del _font_image # Image was copied, and is no longer needed

for _k in range(256):
    _i1 = _k % 16
    _k1 = _k // 16
    _i2 = 7
    while True:
        if _i2 < 0:
            break
        _k2 = _i1 * 8 + _i2
        _flag1 = True
        _j3 = 0
        while _j3 < 8 and _flag1:
            _l3 = (_k1 * 8 + _j3) * _fi_width
            _j4 = _pixel_data[_k2 + _l3] & 0xff
            if _j4 > 0:
                _flag1 = False
            _j3 += 1
        if not _flag1:
            break
        _i2 -= 1
    if _k == 32:
        _i2 = 2
    CHAR_WIDTH.append(_i2 + 2)

del _pixel_data


COLOR_CODES: list[int] = []

for _l in range(32):
    _j1 = (_l >> 3 & 1) * 85
    _l1 = (_l >> 2 & 1) * 170 + _j1
    _j2 = (_l >> 1 & 1) * 170 + _j1
    _l2 = (_l >> 0 & 1) * 170 + _j1
    if _l == 6:
        _l1 += 85
    if _l >= 16:
        _l1 //= 4
        _j2 //= 4
        _l2 //= 4
    COLOR_CODES.append((_l1 & 0xff) << 16 | (_j2 & 0xff) << 8 | _l2 & 0xff)


ALLOWED_CHARS = ''

with resources.open_text(my_evil_twin, 'font.txt', 'utf-8') as _fp:
    while True:
        _line = _fp.readline()
        if not _line:
            break
        if _line[0] == '#':
            continue
        ALLOWED_CHARS += _line.rstrip('\n')


_font_tex = 0
_x = 0
_y = 0


def draw_text_shadow(s: str, x: int, y: int, color: Color) -> None:
    """WARNING: doesn't work properly"""
    draw_text(s, x + 1, y + 1, color, True)
    draw_text(s, x, y, color, False)


def draw_text(s: str, x: int, y: int, color: Color, is_shadow: bool = False) -> None:
    global _x, _y
    if _font_tex == 0:
        _load_font()
    color_i = (color.a << 24) | (color.r << 16) | (color.g << 8) | color.b
    if not (color_i & 0xfc000000):
        color.r |= 0xff000000
    if is_shadow:
        color_i = (color_i & 0xfcfcfc) >> 2 | color_i & 0xff000000
    glColor4f(
        (color_i >> 16 & 0xff) / 255,
        (color_i >> 8 & 0xff) / 255,
        (color_i & 0xff) / 255,
        (color_i >> 24 & 0xff) / 255
    )
    _x = x
    _y = y
    _draw_text(s, is_shadow)


def _load_font() -> None:
    global _font_tex
    with resources.open_binary(my_evil_twin, 'default_font.png') as fp:
        font = PIL.Image.open(fp).convert('RGBA')

    _font_tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, _font_tex)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, font.width, font.height, 0,
        GL_RGBA, GL_UNSIGNED_BYTE, font.tobytes())


def _draw_text(s: str, is_shadow: bool) -> None:
    global _x
    obfuscated = False
    i = 0
    while i < len(s):
        c = s[i]
        if c == '\u00a7' and i + 1 < len(s): # Minecraft format code
            command_s = s[i + 1].lower()
            if command_s == 'k':
                obfuscated = True
            else:
                command_i = '0123456789abcdefk'.find(command_s)
                obfuscated = False
                if command_i == -1:
                    command_i = 15
                if is_shadow:
                    command_i += 16
                new_color = COLOR_CODES[command_i]
                glColor3f(
                    (new_color >> 16 & 0xff) / 255,
                    (new_color >> 8 & 0xff) / 255,
                    (new_color >> 16 & 0xff) / 255
                )
            i += 2
            continue
        char_index = ALLOWED_CHARS.find(c)
        if obfuscated and char_index > 0:
            while True:
                new_char_index = random.randrange(len(ALLOWED_CHARS))
                if CHAR_WIDTH[char_index] == CHAR_WIDTH[new_char_index]:
                    break
            char_index = new_char_index
        if c == ' ':
            _x += 4
            i += 1
            continue
        if char_index > 0:
            _render_normal_char(char_index + 32)
        # else:
        #     func_44033_a(c)
        i += 1


def _render_normal_char(c: int) -> None:
    global _x
    tex_x = (c % 16) * 8
    tex_y = (c // 16) * 8
    cwidth = CHAR_WIDTH[c] - 0.01
    glBindTexture(GL_TEXTURE_2D, _font_tex)
    glBegin(GL_TRIANGLE_STRIP)
    glTexCoord2f(tex_x / 128, tex_y / 128)
    glVertex2f(_x, _y)
    glTexCoord2f(tex_x / 128, (tex_y + 7.99) / 128)
    glVertex2f(_x, _y + 7.99)
    glTexCoord2f((tex_x + cwidth) / 128, tex_y / 128)
    glVertex2f(_x + cwidth, _y)
    glTexCoord2f((tex_x + cwidth) / 128, (tex_y + 7.99) / 128)
    glVertex2f(_x + cwidth, _y + 7.99)
    glEnd()
    _x += CHAR_WIDTH[c]
