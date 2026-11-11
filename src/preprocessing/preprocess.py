import re
from functools import lru_cache

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

TOKEN = re.compile(r"[^\W_]+")


@lru_cache(maxsize=1)
def _stemmer():
    return StemmerFactory().create_stemmer()


@lru_cache(maxsize=1)
def _stopwords():
    return set(StopWordRemoverFactory().get_stop_words())


@lru_cache(maxsize=200000)
def _stem(token):
    return _stemmer().stem(token)


def tokenize(text):
    return TOKEN.findall(text.lower())


def preprocess(text):
    stop = _stopwords()
    tokens = [t for t in tokenize(text) if t not in stop]
    return [_stem(t) for t in tokens]
