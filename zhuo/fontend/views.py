from django.shortcuts import render

# Create your views here.

def vue_text(request):
    # lambda匿名函数
    la = lambda a,b:a+b
    print(la(3,4))
    # 列表推导式
    rr = [a for a in range(10) if a < 5]
    print(rr)
    # 字典推导式
    dict1 = {'name': '张三', 'age':"18"}
    bb = {b:a for a,b in dict1.items()}
    print(bb)
    # map函数
    d = map(map_aa, [1,2,3])
    print(d)
    list1 = [1,2,3,4,5,6,7,8]
    filt = filter(filter_num, list1)
    # for i in filt:
        # print(i)
    print(filt)
    # print(list(filt))
    abc_list = ['55', '66', '77', 'yy']
    abc34 = [i for i in abc_list if str(i).isdigit()]
    print(abc34)
    # abc2 = ['55']
    # abc3 = []
    # abc1 = sorted(abc_list, key=lambda x: x)
    # print(abc1)
    # print(''.join(abc2))
    # aaaaa = ''.join([i for i in abc3 if i])
    # print(aaaaa)
    allMergedZones = sorted(abc34, key=lambda x: int(x))
    print(allMergedZones)
    return render(request, 'vue_text.html')


def map_aa(a, b, c):
    d = a + b + c
    return d

def filter_num(a):
    # for i in a:
    if a % 2 is 0:
        return True
    else:
        return False