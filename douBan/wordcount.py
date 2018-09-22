import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from scipy.misc import imread

plt.rc('figure', figsize=(15, 15))


book = "D:/WebSpider/douban/movie.txt"
txt = open(book,"r",encoding='utf-8',errors='ignore').read()
txt = txt.replace('\n', '' )
txt = txt.replace(' ', '' )
ls = []
# 自定义连接词的词典
jieba.load_userdict('D:/WebSpider/douban/dick.txt')
words = jieba.lcut(txt)
all_text = '  '
for word in words:
    all_text = all_text + word + '  '
ex = ['电影名称']
counts = {}
for word in words:
    ls.append(word)
    if len(word) == 1:
        continue
    else:
        # 计数并存入counts
        counts[word] = counts.get(word,0)+1
for word in ex:
    counts.pop(word)
# 字典 items() 方法以列表返回可遍历的(键, 值) 元组数组。
items = list(counts.items())
# print(items)
'''
  key = lambda x:x[1] 
    等价于
  def  key(x):
      return x[1]
    # 意思是返回此列表中的第二个元素 
'''
# 按照选择（'title',3）等这种列表中的第二个元素 3 等数字作为排序规则
# reverse = True 降序
items.sort(key = lambda x:x[1], reverse = True)
'''
格式限定符
填充与对齐（填充常跟对齐一起使用）
^、<、>分别代表居中、左对齐、右对齐，后面数字表示宽度
:号后面带填充的字符，只能是一个字符，不指定的话默认是用空格填充
'''
for i in range(100):
    word , count = items[i]

color_mask = imread("D:/WebSpider/douBan/love.jpg")
wzhz = WordCloud(font_path='./fonts/simhei.ttf',#中文字体
                 background_color="black", #背景颜色
                 max_words=2000,# 词云显示的最大词数
                 mask=color_mask,#设置背景图片
                 max_font_size=100, #字体最大值
                 random_state=42).generate(all_text)
plt.imshow(wzhz)
plt.show()