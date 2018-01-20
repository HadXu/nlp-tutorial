import marshal
from math import log
import re


re_eng = re.compile('[a-zA-Z0-9]', re.U)


FREQ = {}
total = 0

with open('jieba.cache','rb') as cf:
	FREQ,total = marshal.load(cf)

s = '到MI京研大厦'

DAG = {}

N = len(s)

for k in range(N):
	templist = []
	i = k
	frag = s[k]

	while i<N and frag in FREQ:
		if FREQ[frag]:
			templist.append(i)
		i += 1
		frag = s[k:i+1]
	if not templist:
		templist.append(k)
	DAG[k] = templist


def calc(sentence,DAG,route):
	N = len(sentence)
	route[N] = (0,0)

	logtotal = log(total)

	for idx in range(N-1,-1,-1):
		route[idx] = [(log(FREQ.get(sentence[idx:x+1]) or 1) - 
			logtotal + route[x+1][0],x) for x in DAG[idx]]

		route[idx] = max(route[idx])

route = {}

calc(s,DAG,route)

# print(route)



# DAG route
def cut_DAG_NO_HMM(sentence):
	x = 0
	N = len(sentence)

	buf = ''

	while x<N:
		y = route[x][1]+1
		l_word = sentence[x:y]

		if re_eng.match(l_word) and len(l_word)==1:
			buf += l_word
			x = y
		else:
			if buf:
				yield buf
				buf = ''
			yield l_word
			x = y
	if buf:
		yield buf
		buf = ''

res = cut_DAG_NO_HMM(s)

print('/'.join(res))

# print(DAG)




