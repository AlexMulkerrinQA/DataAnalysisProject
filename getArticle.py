import os, time, re

print ("Scraping article text...\n")
startTime = time.clock()
numArticles = 0
maxArticles = 100

with open("../wikiDataset/enwiki-20090810-pages-articles.xml") as inFile:
	isArticle = False
	isRedirect = False
	isTextContent = False
	articleTitle = ""
	
	while numArticles < maxArticles:
		line = inFile.readline()
		if line.find("</page>") > 0:
			isArticle = False
			isTextContent = False
			isRedirect = False
			articleTitle = "none"
			outFile.close()

		if isArticle:
			if line.find("<text") > 0: # note text element has attributes attached
				isTextContent = True
				if not isRedirect:
					print articleTitle,
					numArticles += 1
					outFile = open('../wikiDataset/articles/' + str(articleTitle) + '.txt', 'w')

			if isTextContent and not isRedirect:
				text = re.sub("<text[^<]+?>|</text>", '', line)
				#print text
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

endTime = time.clock()
print("\nProcess complete in: " + str(endTime-startTime) +"s" )
print("Articles found: " + str(numArticles) )
