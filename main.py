import re
from collections import Counter
from pathlib import Path

from pipe import where
from pprint import pprint


def read_words(file: str) -> list[str]:
    return Path(file).open(encoding="utf8").read().splitlines()


def make_suggestions(possible_words: list[str], cur_state: str, grey: str, yellow: str):
    unknown_positions = [i for i in range(5) if cur_state[i] == "."]
    unknown_chars = lambda x: set(x[i] for i in unknown_positions)

    grey_set = set(grey)
    yellow_set = set(ch for ch in yellow if ch != ".")
    # yellow_pos = set(enumerate(yellow))

    words = list(
        possible_words
        | where(lambda x: re.match(cur_state, x))
        | where(lambda x: unknown_chars(x) & grey_set == set())
        | where(lambda x: unknown_chars(x) & yellow_set == yellow_set)
        | where(lambda x: set(enumerate(x)) & set(enumerate(yellow)) == set())
    )

    counters = [Counter(w[i] for w in words) for i in unknown_positions]
    suggestions = sorted(
        words,
        key=lambda w: sum(counter[char] for counter in counters for char in unknown_chars(w)),
        reverse=True,
    )

    print(len(suggestions))

    return suggestions


if __name__ == "__main__":
    cur_state = "....."
    grey = ""
    yellow = "....."
    # print top 10 suggesttions
    pprint(make_suggestions(read_words("./data/wordle.main.txt"), cur_state, grey, yellow)[:10])
