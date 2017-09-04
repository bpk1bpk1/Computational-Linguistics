inputList = []
#Creating a dictionary with bigrams
def creatingBigrams(inputList):
    bigramsCounter = {}
    firstWord = "Start"
    for secondWord in inputList:
        bigram = firstWord + ' ' + secondWord
        if bigram in bigramsCounter:
            bigramsCounter[bigram] += 1
        else:
            bigramsCounter[bigram] = 1
        firstWord = secondWord
    return bigramsCounter

#Counting the wordcounts in the Input List
def wordCount(inputList):
    wordCount_dictionary= {}
    wordCount_dictionary = {i: inputList.count(i) for i in inputList}
    return wordCount_dictionary

#Calculating Bigram Probabilities
def calculatingProbability(bigramDict,countDict):
    bigramProbability = {}
    for bigram in bigramDict.items():
        bigramWord = (bigram[0].split(' '))
        previousWord = bigramWord[0]
        bigramCount = bigram[1]
        if previousWord in countDict:
            wordOccurence = countDict[previousWord]
            probability = bigramCount/wordOccurence
            if(probability == 1):
                bigramProbability[bigram] = 0.999999
            else:
                bigramProbability[bigram] = probability
        else:
            #Making the probability a really small number
            bigramProbability[bigram] = 0.000001
    return bigramProbability
#Main Function
#Reading all the words from the file and creating an input list of words
with open('nonsense.txt', 'r') as inputFile:
    for line in inputFile:
        line = line.strip('\n')
        if(line == ''):
            inputList.append("End")
            inputList.append("Start")
        else:
            inputList.append(line)

bigramDict = creatingBigrams(inputList)
countDict = wordCount(inputList)
probabilityTable = calculatingProbability(bigramDict,countDict)

print ("{:<15} {:<15}".format('Bigram','Probability'))

for item in probabilityTable.items():
    print ("{:<15} {:<15}".format(item[0][0], item[1]))


