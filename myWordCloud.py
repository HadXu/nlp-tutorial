#coding:utf-8
""" Minimal Example =============== Generating a 
square wordcloud from the US constitution using default arguments. """ 
from os import path 
from wordcloud import WordCloud 
d = path.dirname(__file__)

# Read the whole text. 此处原为处理英文文本，我们修改为传入中文数组 
#text = open(path.join(d, 'constitution.txt')).read() 
frequencies = [(u'知乎',100),(u'小段同学',4),(u'曲小花',3),(u'中文分词',2),(u'样例',1)] 
# Generate a word cloud image 此处原为 text 方法，我们改用 frequencies 
#wordcloud = WordCloud().generate(text) 
wordcloud = WordCloud(font_path = 'MSYH.TTF').fit_words(frequencies)
# Display the generated image: # the matplotlib way: 
import matplotlib.pyplot as plt
plt.imshow(wordcloud) 
plt.axis("off") 
# take relative word frequencies into account, lower max_font_size 
#wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(text) 
wordcloud = WordCloud(font_path = 'MSYH.TTF',max_font_size=40, relative_scaling=.5).fit_words(frequencies) 
plt.figure() 

plt.imshow(wordcloud) 
plt.axis("off") 
plt.show() 
# The pil way (if you don't have matplotlib) 
#image = wordcloud.to_image() 
#image.show()
