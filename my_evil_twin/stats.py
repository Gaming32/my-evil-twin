import math
import random
from typing import Union

import numpy as np

StatsType = list[Union[int, float]]


def load_stats() -> StatsType:
    stats: StatsType = []

    print('Reading stats')
    try:
        with open('met_stats.txt') as fp:
            for line in fp:
                line = line.strip()
                if not line:
                    continue
                stat_type = line[0]
                if stat_type == 'i':
                    content = line[1:]
                    stats.append(int(content, 36) >> 3)
                elif stat_type == 'f':
                    content = line[1:]
                    stats.append(float.fromhex(content))
                elif stat_type == '!':
                    stats.append(math.nan)
                else:
                    print('Unknown stat type, skipping:', stat_type)
    except Exception as e:
        print(f'Failed to read stats, using defaults: {e.__class__.__qualname__}: {e}')
    else:
        print('Stats read')

    stat_types = [(0, int), (0, int), (0, int)]
    for (i, (default, correct_type)) in enumerate(stat_types):
        if i >= len(stats):
            stats.append(default)
        elif math.isnan(stats[i]):
            print('Stat reset requested at index', i)
            stats[i] = default
        elif not isinstance(stats[i], correct_type):
            print(
                'Found incorrect stat type ',
                stats[i].__class__.__qualname__,
                ' expected ',
                correct_type.__qualname__,
                ' at index ',
                i,
                '. using default value.',
                sep=''
            )
            stats[i] = default
    if len(stats) > len(stat_types):
        print(f'Stats data bigger than expected ({len(stats)}>{len(stat_types)}).'
            ' It has been truncated.')
        del stats[len(stat_types):]

    return stats


def write_stats(stats: StatsType) -> None:
    print('Writing stats')
    try:
        with open('met_stats.txt', 'w') as fp:
            for stat in stats:
                if isinstance(stat, int):
                    encoded = (stat << 3) + random.randrange(1 << 3)
                    line = f'i{np.base_repr(encoded, 36)}'
                elif isinstance(stat, float):
                    line = f'f{stat.hex()}'
                else:
                    print('Unknown stat type, skpping:', type(stat))
                    continue
                fp.write(f'{line}\n')
    except Exception as e:
        print(f'Failed to write stats: {e.__class__.__qualname__}: {e}')
    else:
        print('Stats written')
