import re
import marshal
import sys
from math import log

from prob_start import P as start_P
from prob_trans import P as trans_P
from prob_emit import P as emit_P


re_eng = re.compile('[a-zA-Z0-9]', re.U)
re_han = re.compile("([\u4E00-\u9FA5]+)")
re_skip = re.compile("(\d+\.\d+|[a-zA-Z0-9]+)")



FREQ = {}
total = 0

with open('jieba.cache','rb') as cf:
	FREQ,total = marshal.load(cf)

def get_DAG(sentence):
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
	return DAG

def calc(sentence,DAG,route):
	N = len(sentence)
	route[N] = (0,0)

	logtotal = log(total)

	for idx in range(N-1,-1,-1):
		route[idx] = [(log(FREQ.get(sentence[idx:x+1]) or 1) - 
			logtotal + route[x+1][0],x) for x in DAG[idx]]

		route[idx] = max(route[idx])


"""
状态值(隐状态)集合有4种，分别是B,M,E,S，对应于一个汉字在词语中的地位即B（开头）,
M（中间 ),E（结尾）,S（独立成词）
"""
MIN_FLOAT = -3.14e100

PrevStatus = {
	'B':'ES',
	'M':'MB',
	'S':'SE',
	'E':'BM'
}




def viterbi(obs,states,start_p, trans_p, emit_p):
	V = [{}]
	path = {}

	"""
	emit_p 发射概率(当前状态(BESM)到观察其他词的概率)

	"""

	for y in states:
		V[0][y] = start_p[y]+emit_p[y].get(obs[0],MIN_FLOAT)
		path[y] = [y]
	for t in range(1,len(obs)):
		V.append({})
		newpath = {}
		for y in states:
			em_p = emit_p[y].get(obs[t], MIN_FLOAT)
		# t时刻状态为y的最大概率(从t-1时刻中选择到达时刻t且状态为y的状态y0)
			(prob, state) = max([(V[t - 1][y0] + trans_p[y0].get(y, MIN_FLOAT) + em_p, y0) for y0 in PrevStatus[y]])
			V[t][y] = prob
			newpath[y] = path[state] + [y] # 只保存概率最大的一种路径
		path = newpath
		# 求出最后一个字哪一种状态的对应概率最大，最后一个字只可能是两种情况：E(结尾)和S(独立词)  
	(prob, state) = max((V[len(obs) - 1][y], y) for y in 'ES')

	return (prob, path[state])

def __cut(sentence):

	# viterbi算法得到sentence 的切分
	prob, pos_list = viterbi(sentence, 'BMES', start_P, trans_P, emit_P)

	begin, nexti = 0, 0
	print(prob, pos_list)
	for i, char in enumerate(sentence):
		pos = pos_list[i]
		if pos == 'B':
			begin = i
		elif pos == 'E':
			yield sentence[begin:i + 1]
			nexti = i + 1
		elif pos == 'S':
			yield char
			nexti = i + 1
	if nexti < len(sentence):
		yield sentence[nexti:]




def cut_DAG_NO_HMM(sentence):

	DAG = get_DAG(sentence)
	route = {}
	calc(sentence,DAG,route)
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





def cut(sentence):
	blocks = re_han.split(sentence)
	for blk in blocks:
		if re_han.match(blk): # 汉语块
			print(blk)
			for word in __cut(blk):# 调用HMM切分
				yield word
		else:
			tmp = re_skip.split(blk)
			for x in tmp:
				if x:
					yield x




if __name__ == '__main__':
	s = '京研'
	res = cut_DAG_NO_HMM(s)
	print('/'.join(res))
	res = cut(s)
	print('/'.join(res))











