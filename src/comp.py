import logging
import pandas as pd
import argparse
import time


def main():
    """
    Subtract values in tab-separated CSV files.
    """

    # Get the arguments
    parser = argparse.ArgumentParser(
                    prog = 'diff.py',
                    description = 'What the program does',
                    epilog = """Subtract values in tab-separated CSV files.

    Usage:
        diff.py [-a] <targetFile> <valueFile1> <valueFile2> <outPath>

    Arguments:
        <targetFile> = target strings in first column
        <valueFile1> = strings in first column and values in second column
        <valueFile2> = strings in first column and values in second column
        <outPath> = output path for result file

    Options:
        -a, --abs  store absolute (always positive) instead of raw difference

    Note:
        Assumes tap-separated CSV files as input. Appends nan if target is not present in valueFiles.

    """)
    parser.add_argument('valueFile1')           # positional argument
    parser.add_argument('valueFile2')           # positional argument
    parser.add_argument('outPath')           # positional argument
    args = parser.parse_args()


    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    df1 = pd.read_csv(args.valueFile1).set_index("target")
    df2 = pd.read_csv(args.valueFile2).set_index("target")

    diff = df1.subtract(df2, fill_value=0).abs()

    diff["sum"] = diff.mean(axis=1)
    diff["sum"] /= diff["sum"].mean()
    with open(args.outPath, 'w', encoding='utf-8') as f_out:
        for k,v in diff["sum"].items():
            f_out.write(f"{k}\t{v}\n")

    logging.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
