from src import shingles

def test_shingles(benchmark):
    result = benchmark(shingles.main, [
        "-k 6",
        "data/latin/corpus1/lemma",
        "data/latin/targets.txt",
        "data/results/latin/shingles.csv",
        ])
