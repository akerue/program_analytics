# _*_coding:utf-8_*_

import os
import pickle
import argparse

DATA_FILE = "database/data.dat"


def getArgs():
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        "-i", "--init",
        dest="init_flag",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "-d", "--display",
        dest="display_flag",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "-l", "--length",
        dest="length_flag",
        action="store_true",
        default=False,
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = getArgs()

    if args.init_flag:
        os.remove(DATA_FILE)
        with open(DATA_FILE, "wb") as f:
            pass

    if args.display_flag:
        try:
            with open(DATA_FILE, "rb") as f:
                codebooks = pickle.load(f)
        except EOFError:
            codebooks = []

        print codebooks

    if args.length_flag:
        try:
            with open(DATA_FILE, "rb") as f:
                codebooks = pickle.load(f)
        except EOFError:
            codebooks = []

        print len(codebooks)

