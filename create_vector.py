# _*_coding:utf-8_*_

import pickle
import argparse

from nltk.util import ngrams
from nltk import FreqDist

DATA_FILE = "data.dat"


def getArgs():
    """
    コマンド引数をパースします
    """
    parser = argparse.ArgumentParser(description="train the unigram language model")

    # デバック用にファイル一つを指定できるものを用意
    parser.add_argument(
        "-n",
        dest="N",
        required=True,
        type=int,
    )

    # 複数のプログラムが用意されたフォルダを指定すると全てのファイルを読み込む
    parser.add_argument(
        "--source",
        default=None,
        type=str,
        dest="source"
    )

    return parser.parse_args()

def create_freqdist(codebooks, n):
    bag_of_ngrams = []
    fdist = FreqDist()

    for codebook in codebooks:
        bag_of_ngrams.extend(ngrams(codebook, n))

    return FreqDist(bag_of_ngrams)

if __name__ == "__main__":
    args = getArgs()

    with open(DATA_FILE, "rb") as d:
        codebooks = pickle.load(d)

    fd = create_freqdist(codebooks, args.N)
    fd.plot(100)
