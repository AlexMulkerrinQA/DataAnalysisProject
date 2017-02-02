import os, time, re

print ("finding article count...\n")
startTime = time.clock()
numArticles = 0
maxLines = 4000
outFile = open('articleText.txt', 'w')
with open("../wikiDataset/enwiki-20090810-pages-articles.xml") as inFile:
	isArticle = False
	isRedirect = False
	articleTitle = ""
	isTextContent = False
	for i in range(maxLines):
		line = inFile.readline()
		if line.find("</page>") > 0:
			isArticle = False
			isTextContent = False
			isRedirect = False
			articleTitle = "none"

		if isArticle:
			if line.find("<text") > 0: # note text element has attributes attached
				isTextContent = True
				if not isRedirect:
					print articleTitle,
					numArticles += 1

				#	print "(R)",
				#print ""
			if isTextContent and not isRedirect:
				text = re.sub("<text[^<]+?>|</text>", '', line)
				print text
				print outFile.write(text)

			#check for title
			if line.find("<title>") > 0:
				articleTitle = re.sub('<[^<]+?>|\n|\t|^ +', '', line)

			#check if page is redirect
			if line.find("<redirect />") > 0:
				isRedirect = True

		if line.find("</text>") > 0:
			isTextContent = False

		if line.find("<page>") > 0:
			isArticle = True
#			numArticles += 1

endTime = time.clock()
print("\nCount complete in: " + str(endTime-startTime) )
print("Articles found: " + str(numArticles) )
