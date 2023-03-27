import os
import jieba
from collections import Counter
import math
import re

def read_txt(path):
    # 定义文件导入函数
    TXT = []
    result = []
    TXT.append(path)
    while len(TXT) != 0:  # 栈空代表访问完成
        path = TXT.pop()
        try:
            temp_name2 = os.listdir(path)
            for eve in temp_name2:
                TXT.append(path + "\\" + eve)  # 维持绝对路径的表达
        except NotADirectoryError:
            result.append(path)
    return result
path_list = read_txt(r"C:\Users\feng\Desktop\深度学习作业一\jyxstxtqj_downcc.com")
# path_list 为所有小说文件的路径列表
corpus = []
for path in path_list:
    with open(path, "r", encoding="ANSI") as file:
        text = [line.strip("\n").replace("\u3000", "").replace("\t", "") for line in file][3:]
        corpus += text
# corpus 存储语料库，其中以每一个自然段为一个分割
file_stop = r'停词表.txt'
corpus1 = []
stop = []
x = 0
stop1 = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:：.;「<=>?@，．。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
for j in range(len(corpus)):
    corpus[j] = re.sub(stop1, "", corpus[j])
with open(file_stop,'r',encoding='utf-8') as f :
    lines = f.readlines()  # lines是list类型
    for line in lines:
        lline = line.strip()
        stop.append(lline)
for i in range(0,len(corpus)):
    for word in corpus[i].split():
        corpus1.append(word)

for i in stop:
    if i in corpus1:
        while x > len(corpus1):
           corpus1[x].replace(i,"")
           x += 1


with open("处理后的文本.txt", "w", encoding="utf-8") as f:
    for line in corpus1:
        if len(line) > 1:
            print(line, file=f)
with open("处理后的文本.txt", "r", encoding="utf-8") as f:
    text1 = [eve.strip("\n") for eve in f]
# 1-gram
token = []
for para in text1:
    token += jieba.lcut(para)
token_num = len(token)
ct = Counter(token)
vocab1 = ct.most_common()
entropy_1gram = sum([-(eve[1]/token_num)*math.log((eve[1]/token_num),2) for eve in vocab1])
print("词库总词数：", token_num, " ", "词的种类数目：", len(vocab1))
print("出现频率前5的1-gram词语：", vocab1[:5])
print("1gram:", entropy_1gram)

def is_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False
# 2-gram
def combine2gram(cutword_list):
    if len(cutword_list) == 1:
        return []
    res = []
    for i in range(len(cutword_list)-1):
        res.append(cutword_list[i] + " " + cutword_list[i+1])
    return res
token_2gram = []
for para in corpus:
    cutword_list = jieba.lcut(para)
    token_2gram += combine2gram(cutword_list)

# 2-gram的频率统计
token_2gram_num = len(token_2gram)
ct2 = Counter(token_2gram)
vocab2 = ct2.most_common()
# 2-gram相同句首的频率统计
same_1st_word = [eve.split(" ")[0] for eve in token_2gram]
assert token_2gram_num == len(same_1st_word)
ct_1st = Counter(same_1st_word)
vocab_1st = dict(ct_1st.most_common())
entropy_2gram = 0

for eve in vocab2:
    p_xy = eve[1]/token_2gram_num
    first_word = eve[0].split(" ")[0]
    # p_y = eve[1]/vocab_1st[first_word]
    entropy_2gram += -p_xy*math.log(eve[1]/vocab_1st[first_word], 2)
Word = [[0]*2 for i in range(5)]
i = 0
j = 1
while True:
    Word[i][0] = vocab2[j][0]
    Word[i][1] = vocab2[j][1]
    Word[i][0] = Word[i][0].replace(' ', '')

    if not is_contain_chinese(Word[i][0]):
        j = j+1
        continue
    i = i+1
    j = j+1
    if i == 5:
        break
print("词库总词数：", token_2gram_num, " ", "词的种类数目：", len(vocab2))
print("出现频率前5的2-gram词语：", Word)
print("2gram:", entropy_2gram)


# 3-gram
def combine3gram(cutword_list):
    if len(cutword_list) <= 2:
        return []
    res = []
    for i in range(len(cutword_list)-2):
        res.append(cutword_list[i] + cutword_list[i+1] + " " + cutword_list[i+2] )
    return res

token_3gram = []
for para in corpus:
    cutword_list = jieba.lcut(para)
    token_3gram += combine3gram(cutword_list)
# 3-gram的频率统计
token_3gram_num = len(token_3gram)
ct3 = Counter(token_3gram)
vocab3 = ct3.most_common()

# 3-gram相同句首两个词语的频率统计
same_2st_word = [eve.split(" ")[0] for eve in token_3gram]
assert token_3gram_num == len(same_2st_word)
ct_2st = Counter(same_2st_word)
vocab_2st = dict(ct_2st.most_common())
entropy_3gram = 0
for eve in vocab3:
    p_xyz = eve[1]/token_3gram_num
    first_2word = eve[0].split(" ")[0]
    entropy_3gram += -p_xyz*math.log(eve[1]/vocab_2st[first_2word], 2)
Word1 = [[0]*2 for i in range(5)]
i = 0
j = 1
while True:
    Word1[i][0] = vocab3[j][0]
    Word1[i][1] = vocab3[j][1]
    Word1[i][0] = Word1[i][0].replace(' ', '')
    if not is_contain_chinese(Word1[i][0]):
        j = j+1
        continue
    i = i+1
    j = j+1
    if i == 5:
        break
print("词库总词数：", token_3gram_num, " ", "词的种类数目：", len(vocab3))
print("出现频率前5的3-gram词语：", Word1)
print("3gram:", entropy_3gram)
