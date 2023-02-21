import pyximport
pyximport.install(language_level=3)
import cythonfn
from hashlib import blake2s

def shingles(list sentences, list targets, int k=3, int w=3):
    """TODO: Docstring for singles.

    :sentence: TODO
    :k: TODO
    :returns: TODO

    """
    cdef int i, j, index
    cdef dict shingles = {}, hashSet = {}
    cdef str string, word
    cdef list sentence
    for index, word in enumerate(sentences):
        if word in targets:
            if word not in shingles: shingles[word] = {}
            sentence = sentences[index-w:index+w]
            for i in range(1, k+1):
                for j in range(len(sentence)-i+1):
                    string = " ".join(sentence[j:j+i])
                    # compute deterministic hash
                    string = blake2s(string.encode(), digest_size=2).hexdigest()
                    if string in shingles[word]:
                        shingles[word][string] += 1
                    else:
                        shingles[word][string] = 1
                    hashSet[string] = 1
    return shingles, hashSet
