from __future__ import print_function

import sys

if sys.version_info < (3, 9):
    print('This game requires Python 3.9 or later.')
    sys.exit(1)

DEPENCENCIES: list[tuple[str, str]] = [
    ('pygame', 'pygame'),
    ('OpenGL', 'pyopengl'),
    ('OpenGL_accelerate', 'pyopengl-accelerate'),
    ('numpy', 'numpy'),
    # typing-extensions requires special code to check the version
    ('PIL', 'pillow')
]


missing_dependencies: list[str] = []

for dep in DEPENCENCIES:
    try:
        __import__(dep[0])
    except ImportError:
        missing_dependencies.append(dep[1])

try:
    from typing_extensions import NotRequired
except ImportError:
    missing_dependencies.append('typing-extensions>=4.1.0')

if missing_dependencies:
    print('You appear to be missing the following dependencies:')
    for dep in missing_dependencies:
        print('+', dep)
    answer = input('Would you like to install them? [Y/n] ').lower()
    if not answer or answer[0] != 'n':
        import subprocess
        result = subprocess.run(['pip', 'install'] + missing_dependencies)
        if result.returncode:
            print('Failed to install dependencies.')
            sys.exit(1)
    else:
        answer = input('Would you like to try to run the game anyway? [y/N] ').lower()
        if not answer or answer[0] != 'y':
            print('Ok, cancelling.')
            sys.exit(1)

import my_evil_twin.main
