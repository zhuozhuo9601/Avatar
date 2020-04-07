import jieba


split_data = '我们是一个诚实的人'  # 要被切割的数据

res = jieba.cut(split_data,cut_all=True)

print(res)  # <generator object Tokenizer.cut at 0x0000000009EA27D8> 拿到一个生成器

for value in res:
    print(value)