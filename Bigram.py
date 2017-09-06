#This program helps calculate the bigram probabilities from a file.
#The start of a bigram is depicted by <s>
#The end of a bigram is depicted by </s>
from __future__ import division
from __future__ import print_function
from itertools import permutations
from random import choice

#data structures
wordCount = {}
bigramsCount = {}
allbigrams = {}
vocab = set()
bigramprob = {}
smoothedprob = {}

#variables
start = '<s>'
end = '</s>'
vocab.add(start)
vocab.add(end)
#included the test sentences in here. can be read from file if needed
test = ['I do not like them in a mouse .', 'I am Sam I am Sam', 'I do like them anywhere .', 'I would like green ham and beef .']

#Collect bigrams count and vocabulary from text file given as input
prev = start
wordCount[start] = 0
wordCount[end] = 0
with open('nonsense.txt', 'r') as inputFile:
    for line in inputFile:
        #end of line, append </s>
        if line == ' \n' or line == '\n':
            if (prev, end) in bigramsCount:
                bigramsCount[(prev, end)] = bigramsCount[(prev, end)] + 1
            else:
                bigramsCount[(prev, end)] = 1
            if line in wordCount:
                wordCount[line] = wordCount[line] + 1
            else:
                wordCount[line] = 1
            prev = start
            wordCount[end] = wordCount[end] + 1
            wordCount[start] = wordCount[start] + 1
        #start or middle of sentence
        else:
            line = line.strip()
            if (prev, line) in bigramsCount:
                bigramsCount[(prev, line)] = bigramsCount[(prev, line)] + 1
            else:
                bigramsCount[(prev, line)] = 1
            vocab.add(line)
            if line in wordCount:
                wordCount[line] = wordCount[line] + 1
            else:
                wordCount[line] = 1
            prev = line

#check
#print("Vocabulary before test (size {}): \n{}\n".format(len(vocab), vocab))
#print("Training data bigram set (size {}): \n{}\n".format(len(bigramsCount), bigramsCount))
#print("Word count before test (size {}) : \n{}\n".format(len(wordCount), wordCount))

#calculate bigram probabilities using training data(bigramsCount)
for bg in bigramsCount:
    p = bigramsCount[bg]
    p = p/wordCount[bg[0]]
    if p == 0:
        bigramprob[bg] = 0.0000000000000001
    elif p == 1:
        bigramprob[bg] = 0.9999999999999999
    else:
        bigramprob[bg] = p
'''
#check
print ("{:<30} {:<30}".format('Bigram','Probability'))
for item in bigramprob:
    #print(item,bigramprob[item])
    print ("{!s:<30} {:<30}".format(item,bigramprob[item]))
#print("Bigram probabilities before test (size {}): \n{}\n".format(len(bigramprob), bigramprob))
'''

#add test case words to vocabulary and generate test case bigram counts
wordCount[start] = wordCount[start] + len(test)
wordCount[end] = wordCount[end] + len(test)
for line in test:
    line = line.strip().split()
    prev = start
    #collect bigram counts into test dict
    for word in line:
        if (prev, word) in bigramsCount:
            bigramsCount[(prev, word)] = bigramsCount[(prev, word)] + 1
        else:
            bigramsCount[(prev, word)] = 1
        if word in wordCount:
            wordCount[word] = wordCount[word] + 1
        else:
            wordCount[word] = 1
        #add test data into vocabulary for smoothing
        vocab.add(word)
    #add last word and </s> for completeness
    if (line[-1], end)in bigramsCount:
        bigramsCount[(line[-1], end)] = bigramsCount[(line[-1], end)] + 1
    else:
        bigramsCount[(line[-1], end)] = 1
'''
print ("{:<30} {:<30}".format('Bigram','Probability'))
for item in bigramprob:
    #print(item,bigramprob[item])
    print ("{!s:<30} {:<30}".format(item,bigramprob[item]))
'''

#generate all possible bigrams from vocabulary and add counts to bigramsCount
for p in permutations(vocab, 2):
    if p in bigramsCount:
        allbigrams[p] = bigramsCount[p] + 1
    else:
        allbigrams[p] = 1

#check
#print("Generated bigrams (size {}): \n{}\n".format(len(allbigrams), allbigrams))
for i in range(10):
    p = choice(list(bigramsCount))
    if bigramsCount[p] + 1 != allbigrams[p]:
        print("Count error")
        break

#calculate bigram probabilities using allbigrams dict
for bg in allbigrams:
    smoothedprob[bg] = allbigrams[bg]/wordCount[bg[0]]

print ("{:<30} {:<30}".format('Bigram','Probability'))
for item in smoothedprob:
    #print(item,bigramprob[item])
    print ("{!s:<30} {:<30}".format(item,smoothedprob[item]))