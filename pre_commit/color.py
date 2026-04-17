from __future__ import annotations

import argparse
import os
import sys

if sys.platform == 'win32':  # pragma: no cover (windows)
    def _enable() -> None:
        pass

    try:
        _enable()
    except OSError:
        terminal_supports_color = False
    else:
        terminal_supports_color = True
else:  # pragma: win32 no cover
    terminal_supports_color = True

RED = '\033[41m'
GREEN = '\033[42m'
YELLOW = '\033[43;30m'
TURQUOISE = '\033[46;30m'
SUBTLE = '\033[2m'
NORMAL = '\033[m'


def format_color(text: str, color: str, use_color_setting: bool) -> str:
    """Format text with color.

    Args:
        text - Text to be formatted with color if `use_color`
        color - The color start string
        use_color_setting - Whether or not to color
    """
    if use_color_setting:
        return f'{color}{text}{NORMAL}'
    else:
        return text


COLOR_CHOICES = ('auto', 'always', 'never')


def use_color(setting: str) -> bool:
    """Choose whether to use color based on the command argument.

    Args:
        setting - Either `auto`, `always`, or `never`
    """
    if setting not in COLOR_CHOICES:
        raise ValueError(setting)

    return (
        setting == 'always' or (
            setting == 'auto' and
            sys.stderr.isatty() and
            terminal_supports_color and
            os.getenv('TERM') != 'dumb'
        )
    )


def add_color_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '--color', default=os.environ.get('PRE_COMMIT_COLOR', 'auto'),
        type=use_color,
        metavar='{' + ','.join(COLOR_CHOICES) + '}',
        help='Whether to use color in output.  Defaults to `%(default)s`.',
    )
