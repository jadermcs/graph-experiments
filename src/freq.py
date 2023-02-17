from collections import defaultdict
from gensim.models.word2vec import PathLineSentences
import time
import logging
import argparse


def main():
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

    """)
    parser.add_argument('-n', '--norm', action='store_true')      # option that takes a value
    parser.add_argument('corpDir')           # positional argument
    parser.add_argument('testset')           # positional argument
    parser.add_argument('outPath')           # positional argument
    args = parser.parse_args()


    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()


    # Get sentence iterator
    sentences = PathLineSentences(args.corpDir)

    # Initialize frequency dictionary
    freqs = defaultdict(int)

    # Iterate over sentences and words
    corpusSize = 0
    for sentence in sentences:
        for word in sentence:
            corpusSize += 1
            freqs[word] = freqs[word] + 1

    # Load targets
    with open(args.testset, 'r', encoding='utf-8') as f_in:
            targets = [line.strip() for line in f_in]

    # Write frequency scores
    with open(args.outPath, 'w', encoding='utf-8') as f_out:
        for word in targets:
            if word in freqs:
                if args.norm:
                    freqs[word]=float(freqs[word])/corpusSize # Normalize by total corpus frequency
                f_out.write('\t'.join((word, str(freqs[word])+'\n')))
            else:
                f_out.write('\t'.join((word, 'nan'+'\n')))


    logging.info('tokens: %d' % (corpusSize))
    logging.info('types: %d' % (len(freqs.keys())))
    logging.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
