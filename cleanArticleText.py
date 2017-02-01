import os, re, HTMLParser

inFile = open('articleText.txt','r')
outFile = open('cleanedText.txt', 'w')
sentences = re.split(r'\n', inFile.read())

def unescapeHTML(string):
	string = string.replace("&lt;", "<")
	string = string.replace("&gt;", ">")
	string = string.replace("&quot;", '"')
	#string = string.replace("&nbsp;", " ") BUG not being replaced?
	#lastly ampersand
	string = string.replace("&amp;", "&")
	return string
	
for sentence in sentences:
	cleanedSentence = unescapeHTML(sentence)
	outFile.write(cleanedSentence+"\n")
	#words = re.findall(r"[\w']+", sentence)

outFile.close()
inFile.close()

