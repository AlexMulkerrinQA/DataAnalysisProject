import os, time

print ("finding article count...")
startTime = time.clock()
numArticles = 0
maxLines = 400
with open("../wikiDataset/enwiki-20090810-pages-articles.xml") as inFile:
	isArticle = False
	isTextContent = False
	for i in range(maxLines):
		line = inFile.readline()
		if line.find("</page>") > 0:
			isArticle = False
			isTextContent = False

		if isArticle:
			if line.find("<text") > 0: # note text element has attributes attached
				isTextContent = True
			if isTextContent:
				print line,

		if line.find("</text>") > 0:
			isTextContent = False

		if line.find("<page>") > 0:
			isArticle = True
			numArticles += 1

endTime = time.clock()
print("Count complete in: " + str(endTime-startTime) )
print("Articles found: " + str(numArticles) )
