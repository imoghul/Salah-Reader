import docx2txt,re

def doc2words(doc):
	text = docx2txt.process(doc)
	words = text.split(" ")
	while True:
		try:
			words.remove('')
		except:
			break
	words2 = []
	for i in words:
			for j in re.split('\n|\t',i):
				if(j!=''):words2.append(j)
	return words2

def processWords(words):
	outlist = {}
	for i in range(len(words)):
		if words[i] == "AM" or words[i] == "PM":
			if words[i-2].find(")")!=-1:
				days = (words[i-4]+words[i-3]+words[i-2])
			else:
				days = "all"
			time = (words[i-1]+words[i])
			outlist[time] = days
	return outlist

print(processWords(doc2words("iqaamahdoc/Iqaamah Times.docx")))
