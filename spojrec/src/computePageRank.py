from model.spojdata import SubmissionsItem
from crawler.signedlistParser import parseSignedlist

def parse(submissionsItem):
    return parseSignedlist(submissionsItem.data)

def get_acepted_problems(parsedSub):
    acepted = []
    for row in parsedSub:
            if row['RESULT'] == 'AC':
                acepted.append(row['PROBLEM'])
    return acepted

def conpute_page_rank():
    submitions = SubmissionsItem().query().fetch()
    for sub in submitions:
        parsedSub = parse(sub)
        acepted =  get_acepted_problems(parsedSub)
        
                