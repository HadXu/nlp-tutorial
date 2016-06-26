#coding:utf-8

import jieba
from wordcloud import WordCloud 

f = open(u'天龙八部.txt','r').read()
s = {}
f = jieba.cut(f)
for w in f:
	if len(w) > 1:
		previous_count = s.get(w,0)
		s[w] = previous_count+1

word = sorted(s.items(),key=lambda (word,count):count, reverse = True)
word = word[1:100]
#print word[:100]
wordcloud = WordCloud(font_path = 'MSYH.TTF').fit_words(word)
import matplotlib.pyplot as plt
plt.imshow(wordcloud) 
plt.axis("off")
plt.show()
