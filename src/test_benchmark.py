from src import shing

def test_shingles(benchmark):
    result = benchmark(shing.main, [
        "-k 6",
        "data/latin/corpus1/lemma",
        "data/latin/targets.txt",
        "data/results/latin/shingles.csv",
        ])
