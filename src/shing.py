import time
import pickle
import logging
import argparse
import pandas as pd
from shingles import shingles
from gensim.models.word2vec import PathLineSentences

def main(raw_args=None):
    """
    Get frequencies from corpus.
    """

    # Get the arguments
    parser = argparse.ArgumentParser(
                    prog = 'freq.py',
                    description = 'What the program does',
                    epilog = """Get frequencies from corpus.

    Usage:
        freq.py [-n] <corpDir> <testset> <outPath>

    Arguments:

        <corpDir> = path to corpus or corpus directory (iterates through files)
        <testset> = path to file with one target per line
        <outPath> = output path for result file

    Options:
        -n --norm  normalize frequency by total corpus frequency
        -k size of k for shinglings
        -w size of window

    """)
    parser.add_argument('-n', '--norm', action='store_true')      # option that takes a value
    parser.add_argument('corpDir')           # positional argument
    parser.add_argument('testset')           # positional argument
    parser.add_argument('outPath')           # positional argument
    parser.add_argument('-k', default=3, type=int)           # positional argument
    parser.add_argument('-w', default=6, type=int)           # positional argument
    args = parser.parse_args(raw_args)


    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()


    # Get sentence iterator
    sentences = []
    for sentence in PathLineSentences(args.corpDir):
        sentences += sentence

    # Load targets
    with open(args.testset, 'r', encoding='utf-8') as f_in:
            targets = [line.strip() for line in f_in]

    shing, hashSet = shingles(sentences, targets, args.k, args.w)

    out = {"shingles": shing, "hashes": hashSet}
    with open(args.outPath, "wb") as handle:
        pickle.dump(out, handle)

    logging.info('shingles: %d' % (len(hashSet)))
    logging.info('types: %d' % (len(shing.keys())))
    logging.info("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()
