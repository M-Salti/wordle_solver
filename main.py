import re
from collections import Counter
from functools import lru_cache
from pathlib import Path

from pipe import dedup, select, where


@lru_cache
def get_all_words():
    return list(
        Path("/usr/share/dict/words").open().read().splitlines()
        | select(lambda x: x.lower())
        | dedup
        | where(lambda x: re.match("[a-z]{5}$", x))
    )


def make_suggestions(cur_state: str, rejected_chars: str, contains: str):
    unknown_positions = [i for i in range(5) if cur_state[i] == "."]
    unknown_chars = lambda x: set(x[i] for i in unknown_positions)

    words = list(
        get_all_words()
        | where(lambda x: re.match(cur_state, x))
        | where(lambda x: all(r not in unknown_chars(x) for r in rejected_chars))
        | where(lambda x: all(c in unknown_chars(x) for c in contains))
    )

    counters = [Counter(w[i] for w in words) for i in unknown_positions]
    suggestions = sorted(
        words,
        key=lambda w: sum(counter[char] for counter in counters for char in unknown_chars(w)),
        reverse=True,
    )

    print(len(suggestions))

    return suggestions


cur_state = "....."
rejected = ""
contains = ""
print(make_suggestions(cur_state, rejected, contains)[0])
