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

