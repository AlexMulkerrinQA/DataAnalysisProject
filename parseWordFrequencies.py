import os, re, operator

def findWordFreq(inFileName):
	inFile = open('articleTexts/' + inFileName, 'r')
	sentences = re.split(r'\n', inFile.read().lower())
	wordList = {}
	allWordsTotal = 0

	for sentence in sentences:
		words = re.findall(r"[\w']+", sentence)
		for word in words:
			allWordsTotal += 1
			if not (word in wordList):
				wordList[word] = 1
			else:
				wordList[word] += 1

	sortedWordList = sorted(wordList.items(), key=operator.itemgetter(1), reverse=True)
	return sortedWordList

def displayWordList(sortedWordList):
	isFirst = True
	output = ""
	for i in range(20):
		word = sortedWordList[i]
		if not isFirst:
			output += ', '
		else:
			isFirst = False
		output += '"'+str(word[0])+'":'+str(word[1])
	output += '}\n'
	print output

for inFileName in os.listdir('articleTexts'):
	articleTitle = re.sub('.txt', '', inFileName)
	print articleTitle
	
	wordList = findWordFreq(inFileName)
	displayWordList(wordList)
	