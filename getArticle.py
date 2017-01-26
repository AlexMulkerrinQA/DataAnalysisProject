import os, time

print ("finding article count...")
startTime = time.clock()
numArticles = 0
maxLines = 100
with open("../wikiDataset/enwiki-20090810-pages-articles.xml") as inFile:
	isArticle = False
	for line in inFile:
#		line = inFile.readline()
		if line.find("</page>") > 0:
			isArticle = False

	#	if isArticle:
	#		print line,

		if line.find("<page>") > 0:
			isArticle = True
			numArticles += 1

endTime = time.clock()
print("Count complete in: " + str(endTime-startTime) )
print("Articles found: " + str(numArticles) )
