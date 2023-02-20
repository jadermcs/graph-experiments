import logging
import pickle
import argparse
import time
from scipy.spatial import distance


def main():
    """
    Subtract values in tab-separated CSV files.
    """

    # Get the arguments
    parser = argparse.ArgumentParser(
                    prog = 'comp.py',
                    description = 'What the program does',
                    epilog = """Subtract values in tab-separated CSV files.

    Usage:
        comp.py [-a] <valueFile1> <valueFile2> <outClas>

    Arguments:
        <valueFile1> = strings in first column and values in second column
        <valueFile2> = strings in first column and values in second column
        <outClas> = output path for class result file

    Options:
        -a, --abs  store absolute (always positive) instead of raw difference

    Note:
        Assumes tap-separated CSV files as input. Appends nan if target is not present in valueFiles.

    """)
    parser.add_argument('valueFile1')           # positional argument
    parser.add_argument('valueFile2')           # positional argument
    parser.add_argument('outClas')           # positional argument
    args = parser.parse_args()


    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    with open(args.valueFile1, "rb") as fin:
        data = pickle.load(fin)
        key1 = data["hashes"]
        set1 = data["shingles"]

    with open(args.valueFile2, "rb") as fin:
        data = pickle.load(fin)
        key2 = data["hashes"]
        set2 = data["shingles"]

    keys = key1.keys() | key2.keys()

    logging.info("sorting values and inserting zeros.")
    for k in set1:
        values1 = set1[k]
        set1[k] = [values1[skey] if skey in values1 else 0 for skey in keys]
        values2 = set2[k]
        set2[k] = [values2[skey] if skey in values2 else 0 for skey in keys]

    logging.info("computing distance between pairs.")
    preds = {}
    for key in set1:
        sim = distance.cosine(set1[key], set2[key])
        preds[key] = sim

    with open(args.outClas, 'w', encoding='utf-8') as f_out:
        for k in sorted(preds.keys()):
            f_out.write(f"{k}\t{preds[k]}\n")

    logging.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
