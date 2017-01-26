import os

print ("Hello AWS!")
print ("counting lines in title List...")
totalLines=0
with open("../wikiDataset/enwiki-20090810-all-titles-in-ns0") as inFile:
	for line in inFile:
		totalLines += 1

print totalLines
