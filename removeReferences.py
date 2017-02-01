import os, re, HTMLParser

inFile = open('cleanedText.txt','r')
#outFile = open('textOnly.txt', 'w')
#sentences = re.split(r'\n', inFile.read())

wholeText = inFile.read()

isTag = False
#isTextContent = False	
# regexs are confusing... remove single tags and text between ref tag pairs.
# captures opening wiki markup '[[' (with or without | pipe), closing ']]', single html tags <x />, reference elements <ref x>xxx</ref>
regexPattern = """\[\[[^|^\]]+\||
	\[\[|
	\]\]|
	<[^>]+/>|
	<ref.*?>[\s\S]*?</ref>|
	={1,6}"""

#try do this compiled thing, still todo:
#\[\[(File|Category):[\s\S]+\]\]|
#{{[\s\S\n]+?}}|

#(<s>|<!--)[\s\S]+(</s>|-->)|
CompiledRegex = re.compile(r"""
		\[\[[^|^\]]+\||
		\[\[|
		\]\]|
		\'{2,5}|
		\{\{[^\}]+\}\}|
		<[^>]+/>|
		<ref.*?>[\s\S]*?</ref>|
		={1,6}""", re.VERBOSE)
	
#for i in range(5):
	#sentence = sentences[i]
	# out = ""
	# for c in sentence:
		# if c == '<':
			# isTag = True
		# elif c == '>':
			# isTag = False
			
		# elif not isTag:
			# out += c
out = CompiledRegex.sub("_", wholeText)

print out


#outFile.close()
inFile.close()

