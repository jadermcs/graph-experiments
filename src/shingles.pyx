from collections import defaultdict
from gensim.models.word2vec import PathLineSentences
import time
from itertools import chain
import logging
import argparse

def shingles(list sentences, list targets, int k=3):
    """TODO: Docstring for singles.

    :sentence: TODO
    :k: TODO
    :returns: TODO

    """
    cdef int i, j, index, corpusSize = 0
    cdef dict shingles = {}
    cdef str string, word, sentence
    for index, word in enumerate(sentences):
        if word in targets:
            if word not in shingles: shingles[word] = {}
            sentence = " ".join(sentences[index-k:index+k])
            for i in range(2, k+1):
                for j in range(len(sentence)-i):
                    string = sentence[j:j+i]
                    if string not in shingles[word]:
                        shingles[word][string] = 1
                    else: shingles[word][string] += 1
        corpusSize += 1
    return shingles, corpusSize

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

    """)
    parser.add_argument('-n', '--norm', action='store_true')      # option that takes a value
    parser.add_argument('corpDir')           # positional argument
    parser.add_argument('testset')           # positional argument
    parser.add_argument('outPath')           # positional argument
    parser.add_argument('-k', default=6, type=int)           # positional argument
    args = parser.parse_args(raw_args)


    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()


    # Get sentence iterator
    cdef list sentences = []
    for sentence in PathLineSentences(args.corpDir):
        sentences += sentence

    # Initialize frequency dictionary
    cdef dict shing
    cdef int corpusSize

    # Load targets
    with open(args.testset, 'r', encoding='utf-8') as f_in:
            targets = [line.strip() for line in f_in]

    # Iterate over sentences and words
    shing, corpusSize = shingles(sentences, targets, args.k)

    # Write frequency scores
    with open(args.outPath, 'w', encoding='utf-8') as f_out:
        for word in targets:
            if word in shing:
                if args.norm:
                    shing[word]={k:v/corpusSize for k,v in shing[word].items()}
                f_out.write('\t'.join((word, str(shing[word])+'\n')))
            else:
                f_out.write('\t'.join((word, 'nan'+'\n')))


    logging.info('tokens: %d' % (corpusSize))
    logging.info('types: %d' % (len(shing.keys())))
    logging.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
