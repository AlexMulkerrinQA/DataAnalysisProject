import os, re, operator

wordList = {}
allWordsTotal = 0

print ("Parsing file for word frequencies...")

inFile = open('cleanedText.txt','r')
sentences = re.split(r'\n', inFile.read())

for sentence in sentences:
	words = re.findall(r"[\w']+", sentence)
	for word in words:
		allWordsTotal += 1
		if not (word in wordList):
			wordList[word] = 1
		else:
			wordList[word] += 1

print ("Parsed " + str(allWordsTotal) + " words. With " + str(len(wordList)) + " different words encountered")

sortedWordList = sorted(wordList.items(), key=operator.itemgetter(1), reverse=True)

print sortedWordList
