import os, re, HTMLParser

inFile = open('cleanedText.txt','r')
outFile = open('textOnly.txt', 'w')

wholeText = inFile.read()	
# regexs are confusing... remove single tags and text between ref tag pairs.
# captures opening wiki markup '[[' (with or without | pipe), closing ']]', single html tags <x />, reference elements <ref x>xxx</ref>
CompiledRegex = re.compile(r"""
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
	
out = CompiledRegex.sub("", wholeText)
#print out
outFile.write(out)

outFile.close()
inFile.close()

