# _*_coding:utf-8_*_

import pickle
import argparse
import pprint

from Simplexer import Simplexer

from nltk.util import ngrams

VECTOR_FILE = "database/vector.dat"


def getArgs():
    """
    コマンド引数をパースします
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        "--threshould",
        dest="threshould",
        required=True,
        type=float,
    )

    parser.add_argument(
        "-t", "--target",
        required=True,
        type=argparse.FileType("r"),
        dest="target_file"
    )

    return parser.parse_args()

if __name__ == "__main__":
    args = getArgs()

    with open(VECTOR_FILE, "rb") as v:
        conditional_vector = pickle.load(v)

    lexer = Simplexer()

    codebook = lexer.analyze(args.target_file)

    bag_of_ngrams = ngrams(codebook, conditional_vector.N)

    error_count = 0
    for ngram in bag_of_ngrams:
        print ngram
        print conditional_vector.prob(ngram[-1], ngram[:-1])
        if conditional_vector.prob(ngram[-1], ngram[:-1]) < args.threshould:
            print ngram
            error_count += 1
    print error_count
