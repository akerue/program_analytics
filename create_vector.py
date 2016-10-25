# _*_coding:utf-8_*_

import pickle
import argparse
import pprint

from ConditionalVector import ConditionalVector

from nltk.util import ngrams

DATA_FILE = "database/data.dat"
VECTOR_FILE = "database/vector.dat"

def getArgs():
    """
    コマンド引数をパースします
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        "-n",
        dest="N",
        required=True,
        type=int,
    )

    return parser.parse_args()


def create_bon(codebooks, n):
    bag_of_ngrams = []

    for codebook in codebooks:
        bag_of_ngrams.extend(ngrams(codebook, n))

    return bag_of_ngrams


if __name__ == "__main__":
    args = getArgs()

    with open(DATA_FILE, "rb") as d:
        codebooks = pickle.load(d)

    bag_of_ngrams = create_bon(codebooks, args.N)

    cv = ConditionalVector(bag_of_ngrams)

    with open(VECTOR_FILE, "wb") as v:
        pickle.dump(cv, v)
