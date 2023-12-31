import json
import re


def read_file(path: str) -> list[dict]:
    """
    Reads a file with song lyrics and returns a list of song data dictionaries
    """
    with open(path, "r") as f:
        data = json.load(f)
    return data["item"]


def print_lyrics(song: dict) -> None:
    """
    Prints song lyrics
    """
    for line in song["lyrics"]:
        print(line)


def words(song: dict) -> list[str]:
    """
    Cleans song lyrics and returns a list of words
    """
    words = [
        word
        for line in song["lyrics"]
        for word in re.sub(r"[^\w]", " ", line)  # remove punctuation
        .lower()  # lowercase
        .split()  # split by whitespace
    ]
    return words


def stopwords(language: str = "english") -> list[str]:
    """
    Returns a list of stopwords, language = english | polish
    """
    with open(f"{language}.stopwords.txt", "r") as f:
        return f.read().splitlines()


def remove_stopwords(words: list[str]) -> list[str]:
    """
    Returns a list of words without stopwords
    """
    stop = stopwords()
    return [w for w in words if w not in stop]


def counter(words: list[str]) -> dict[str, int]:
    """
    Returns word count dictionary
    """
    word_count = {}
    for w in words:
        if w not in word_count:
            word_count[w] = 1
        else:
            word_count[w] += 1
    return word_count


def add_counters(counter1: dict[str, int], counter2: dict[str, int]) -> dict[str, int]:
    """
    Returs a result of adding two word count dictionaries
    """
    word_count = {w: c for w, c in counter1.items()}
    for w, c in counter2.items():
        if w not in word_count:
            word_count[w] = c
        else:
            word_count[w] += c
    return word_count


def playlist_counter(path) -> dict[str, int]:
    """
    Return a word count dictionary for all songs in the playlist
    """
    try:
        word_count = {}
        data = read_file(path)
        for i, song in enumerate(data):
            w = remove_stopwords(words(song))
            c = counter(w)
            word_count = add_counters(word_count, c)
            print(f"{i+1: < 5}total words: {len(w)},  unique words: {len(c)}")
    except OSError:
        print(f"File not found: {path}")
    except KeyError:
        print(f"Processed all songs from the file: {path}")
    return word_count


def sorted_counter(counter: dict[str, int], threshold: int = 0) -> dict[str, int]:
    """
    Return counter sorted by word frequencies, do not include rare words under threshold
    """
    s = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    f = dict(filter(lambda x: (x[1] >= threshold), s))
    return f


def alphabetical_counter(counter: dict[str, int]) -> dict[str, int]:
    """
    Return counter sorted by word's alphabetical order
    """
    a = dict(sorted(counter.items(), key=lambda x: x[0], reverse=False))
    return a


def print_counter(counter: dict) -> None:
    """
    Print all words and their counts, one line at a time
    """
    for word, count in counter.items():
        print(f"{word: <15}: {count}")
