import os, re, HTMLParser

inFile = open('cleanedText.txt','r')
outFile = open('cleanedText.txt', 'w')
sentences = re.split(r'\n', inFile.read())

	
for sentence in sentences:
	cleanedSentence = unescapeHTML(sentence)
	print cleanedSentence

outFile.close()
inFile.close()

