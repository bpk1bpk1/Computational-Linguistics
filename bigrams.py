from __future__ import division
from __future__ import print_function
from itertools import permutations
from random import choice

bigramsCount = {}
allbigrams = {}
testbigrams = {}
vocab = set()
#included the test sentences in here. can be read from file if needed
test = ['I do not like them in a mouse .', 'I am Sam I am Sam', 'I do like them anywhere .', 'I would like green ham and beef .']

start = '<s>'
end = '</s>'
vocab.add(start)
vocab.add(end)

#collect bigrams count and vocabulary from text file
prev = start
with open('nonsense.txt', 'r') as inputFile:
    for line in inputFile:
        #end of line, append </s>
        if line == ' \n' or line == '\n':
            if (prev, end) in bigramsCount:
                bigramsCount[(prev, end)] = bigramsCount[(prev, end)] + 1
            else:
                bigramsCount[(prev, end)] = 1
            prev = start
        #start or middle of sentence
        else:
            line = line.strip()
            if (prev, line) in bigramsCount:
                bigramsCount[(prev, line)] = bigramsCount[(prev, line)] + 1
            else:
                bigramsCount[(prev, line)] = 1
            vocab.add(line)
            prev = line

#check
print("Vocabulary before test (size {}): \n{}\n".format(len(vocab), vocab))
print("Training data bigram set (size {}): \n{}\n".format(len(bigramsCount), bigramsCount))

#calculate bigram probabilities using training data(bigramsCount)

#add test cases to vocabulary and generate test case bigram counts
for line in test:
    line = line.strip().split()
    prev = start
    #collect bigram counts into test dict
    for word in line:
        if (prev, word) in testbigrams:
            testbigrams[(prev, word)] = testbigrams[(prev, word)] + 1
        else:
            testbigrams[(prev, word)] = 1
        #add test data into vocabulary for smoothing
        vocab.add(word)
    #add last word and </s> for completeness
    if (line[-1], end)in testbigrams:
        testbigrams[(line[-1], end)] = testbigrams[(line[-1], end)] + 1
    else:
        testbigrams[(line[-1], end)] = 1

#check
print("Vocabulary after test (size {}): {}\n".format(len(vocab), vocab))

#generate all possible bigrams from vocabulary
for p in permutations(vocab, 2):
    if p in bigramsCount:
        allbigrams[p] = 1 + bigramsCount[p]
    else:
        allbigrams[p] = 1

#check
print("Generated bigrams (size {}): \n{}\n".format(len(allbigrams), allbigrams))
for i in range(10):
    p = choice(list(bigramsCount))
    if bigramsCount[p] + 1 != allbigrams[p]:
        print("Count error")
        break

#calculate bigram probabilities using allbigrams dict
