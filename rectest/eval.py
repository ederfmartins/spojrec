

def eval_user(user, recProblems, expectedAnswer, topk=5):
	cnt = 0
	hit = 0
	if len(expectedAnswer[user]) > 0:
		for (problem, score) in recProblems:
			if cnt >= topk:
				break
			
			if problem in expectedAnswer[user]:
				hit += 1.0
	
			cnt += 1
		
		return hit/min(len(expectedAnswer[user]), topk)
	else:
		return 0.0
			
