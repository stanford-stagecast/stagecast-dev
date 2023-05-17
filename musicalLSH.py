from scipy.spatial.distance import cosine
from random import randint
import numpy as np
import librosa
import sys
import warnings
warnings.simplefilter(action='ignore')

'''
The minhash function used in local sensitive hashing.

data: the input data to be hashed; should be a list
permutation: the permutatino matrix used; should be the same for source and target with same length
prime/N: optinal parameters for minhash; can be tuned for better accuracy

return value: a list of N ints being the result of hashing
'''
def chromahash(data, permutation, prime = 614889782588491410, N = 128):
    vec = [float('inf') for i in range(N)]

    for val in data:
        # val = hash(val)
        val = librosa.feature.chroma_stft(y=np.array(val).astype("float")).mean()

        for i, (a, b) in enumerate(permutation):
            output = (a * val + b) % prime
            vec[i] = min(vec[i], output)

    return vec

'''
Get the min hash result from data using permutation.

data: the original data to be hashed; should be a list
n: size of units for minhash
l: size of units for comparison
permutation: the permutation matrix; should be the same for source and target with same length

return value: the hashed results of differnet l-grams



eg. (for n and l):
data = [1,2,3,4,5,6,7,8,9,10]
n = 3
l = 5
return value will be [hash for [1,2,3,4,5], hash for [2,3,4,5,6], hash for [3,4,5,6,7], 
                      hash for [4,5,6,7,8], hash for [5,6,7,8,9], hash for [6,7,8,9,10]]
hash for [1,2,3,4,5] is computed by [[1,2,3],[2,3,4],[3,4,5]]
'''
def get_hash(data, n, l, permutation):
    ngrams = [tuple(data[i:i+n]) for i in range(len(data)-n+1)]
    features = [chromahash(sorted(ngrams[i:i+l-n+1]), permutation) for i in range(len(data)-l+1)]
    return [np.array(feature) / max(feature) for feature in features]

'''
Get the hashed results with different sizes of l, ranging from minNotes to maxNotes.

data: the original data to be hashed; should be a list
n: size of units for minhash
minNotes: smallest value of l, inclusive
maxNotes: largest value of l, inclusive

return value: the list of hashed results
'''
def get_notes_hashes(data, n, permutation, minNotes, maxNotes):
    return [get_hash(data, n, x, permutation) for x in range(minNotes, maxNotes+1)]

'''
Get k indices with highest similarity scores comparing to the target interval.

hashed_source_data: output of get_notes_hashes
hashed_target_dat: hashed target
k: optinal parameter indicating the number of indices to return

return value: the list of indices with corresponding elements being the k largest similarity scores, in decreasing order
'''

def get_k_highest_scores(hashed_source_data, hashed_target_data, k = 10):
    scores = [1 - cosine(source, hashed_target_data) for source in hashed_source_data]
    return list(reversed(np.argsort(scores)[-k:]))

'''
An example using the above functions.
'''
if __name__ == '__main__':
    permutation = [(randint(0, sys.maxsize), randint(0, sys.maxsize)) for i in range(128)]
    data = [2,2,3,4,8,8,1,2,3,9,2,2,3,4,8,8,1,2,3,8]
    n = 3
    minNotes = 5
    maxNotes = 10
    temp = get_notes_hashes(data, n, permutation, minNotes, maxNotes)

    sample = [2,2,3,4,8,8,1,2,3,9]
    sampled_hash = get_hash(sample, n, 10, permutation)[0]

    # print similarity scores
    for i, w in enumerate(temp[-1]):
        print('Similarity with {}: {}'.format(data[i:i+10], 1 - cosine(w, sampled_hash)))

    print('selected indices: {}'.format(get_k_highest_scores(temp[-1], sampled_hash,5)))