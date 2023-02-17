from collections import defaultdict

def main():
    """TODO: Docstring for main.
    :returns: TODO

    """
    words = {}
    with open("target_words.txt", "r") as fin:
        for w in fin.readlines():
            k, v = w.strip().split("_")
            words[k] = v

    corpus1 = []
    with open("data/corpus1/token/ccoha1.txt") as c1:
        for line in c1:
            corpus1 += line.strip().split()

    words_in_context = defaultdict(list)

    for index, word in enumerate(corpus1):
        if word in words:
            words_in_context[word].append(" ".join(corpus1[index-6:index+6]))

    for word in words_in_context:
        for context in words_in_context[word]:
            print(word, "\t", context)




if __name__ == "__main__":
    main()
