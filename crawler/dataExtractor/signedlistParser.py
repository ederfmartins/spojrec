# -*- coding: utf-8 -*-

LABEL_PROBLEM_COLUMN = 'PROBLEM'
LABEL_COLUMN_ACCEPTED = 'RESULT'

def parseSignedlist(data):
	readAtributes = False
	readDummyLine = False
	readData = False
	attrs = []
	dataAsList = []
	
	if data is None:
		return None
	
	for line in data.split('\n'):
		if len(line) > 0 and line[0] == '/':
			readAtributes = True
		elif len(line) > 0 and line[0] == '\\':
			readData = False
		elif readAtributes:
			readAtributes = False
			readDummyLine = True
			for attr in line.split('|'):
				attrs.append(attr.strip())
		elif readDummyLine:
			readDummyLine = False
			readData = True
		elif readData and len(line) > 0 and line[0] == '|':
			fields = line.split('|')
			elem = dict()
			for i in range(1, len(fields)):
				elem[attrs[i]] = fields[i].strip()
		
			dataAsList.append(elem)
	
	return dataAsList


if __name__ == "__main__":
	data = str(file('testData.txt').read())
	obj = parseSignedlist(data)
	
	#The test file has 284 submissions
	assert len(obj) == 284
	assert obj[0]['PROBLEM'] == 'TELEMAR7'
	assert obj[283]['PROBLEM'] == 'VARETAS'


	data = str(file('testData1.txt').read())
	obj = parseSignedlist(data)
	
	#The test file has 284 submissions
	assert len(obj) == 26
	assert obj[0]['PROBLEM'] == 'POPULAR'
	assert obj[24]['PROBLEM'] == 'BAFO'
