import os, re, HTMLParser

# regexs are confusing... remove single tags and text between ref tag pairs.
# captures opening wiki markup '[[' (with or without | pipe), closing ']]', single html tags <x />, reference elements <ref x>xxx</ref>
compiledRegex = re.compile(r"""
		\[\[(Image|File):[^\[]+\||
		\[\[Category:[^\]]+\]\]|
		\[\[[^|^\]]+\||
		\[\[|
		\]\]|
		\'{2,5}|
		\{\{[^\}]+\}\}|
		\[[^\]]+\]|
		<[^>]+/>|
		<ref.*?>[\s\S]*?</ref>|
		<!--.*?-->|
		={1,6}""", re.VERBOSE)
	
def unescapeHTML(string):
	string = string.replace("&lt;", "<")
	string = string.replace("&gt;", ">")
	string = string.replace("&quot;", '"')
	#lastly ampersand
	string = string.replace("&amp;", "&")
	return string
	
for inFileName in os.listdir('../wikiDataset/articles'):
	inFile = open('../wikiDataset/articles/' + inFileName, 'r')
	articleTitle = re.sub('.txt', '', inFileName)
	outFile = open('articleTexts/' + articleTitle + '.txt', 'w') 
	
	articletext = inFile.read()
	articletext = unescapeHTML(articletext)
	articletext = compiledRegex.sub("", articletext)
	outFile.write(articletext)
	outFile.close()
	inFile.close()

