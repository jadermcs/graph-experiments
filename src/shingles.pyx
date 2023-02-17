def shingles(list sentences, list targets, int k=3, int w=6):
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
            sentence = " ".join(sentences[index-w:index+w])
            for i in range(2, k+1):
                for j in range(len(sentence)-i):
                    string = sentence[j:j+i]
                    if string not in shingles[word]:
                        shingles[word][string] = 1
                    else: shingles[word][string] += 1
        corpusSize += 1
    return shingles, corpusSize
