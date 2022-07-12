import time
from datetime import datetime, timedelta, date
import numpy as np
import pandas as pd
from scipy import interpolate
data = pd.read_csv('D:\wei.csv')

# 获取数据集中列名为date和value这两列
data = data.loc[:, ['date', 'value']] 
# 标准化日期，获取时间的“年、月、日”
def change_date(s):
    s = datetime.strptime(s, "%Y/%m/%d")  # 把日期标准化，转化结果如：2015/1/4 => 2015-01-04 00:00:00
    s = str(s)  # 上一步把date转化为了时间格式，因此要把date转回str格式
    return s[:10] # 只获取年月日，即“位置10”之前的字符串
data['date'] = data['date'].map(change_date)  # 用change_date函数处理列表中date这一列，如把“2015/1/4”转化为“2015-01-04”
data = data.sort_values(by='date')  # 按date这一列进行排序
xs = data['date'].values
ys = data['value'].values
insert_xs = []
# 获取断开的时间
for i in range(len(xs)):
    if i + 1 == len(xs):
        break
    t1 = int(time.mktime(time.strptime(xs[i], "%Y-%m-%d")))
    t2 = int(time.mktime(time.strptime(xs[i + 1], "%Y-%m-%d")))
    differ = (datetime.fromtimestamp(t2) - datetime.fromtimestamp(t1)).days
    while differ != 1:
        differ -= 1
        tmp = (datetime.fromtimestamp(t2) + timedelta(days=-differ)).strftime("%Y-%m-%d")
        insert_xs.append(tmp)
print(insert_xs)        
def interpolation_data(x, y, kind):
    x, y = list(x), list(y)
    insert_x = []
    for i in range(len(x)):
        if i + 1 == len(x):
            break
        t1 = int(time.mktime(time.strptime(x[i], "%Y-%m-%d")))
        t2 = int(time.mktime(time.strptime(x[i + 1], "%Y-%m-%d")))
        differ = (datetime.fromtimestamp(t2) - datetime.fromtimestamp(t1)).days
        while differ != 1:
            differ -= 1
            tmp = (datetime.fromtimestamp(t2) + timedelta(days=-differ)).strftime("%Y-%m-%d")
            insert_x.append(tmp)    
    # 等于0说明没有断开的时间
    if len(insert_x) == 0:
        return 0    
    # 对断开的数据进行插值，并将原来补0的值替换
    newx = x + insert_x
    newx = sorted(newx)
    
    xdict = {}          # 插值后的时间x
    resx_dict = {}      # 存放插值的结果列表，key：时间，value：ecpm_yesterday
    x_list = []         # 原x转为对应数字
    x_i_list = []       # 待插值x转为对应数字
    j = 0
    for i in range(len(newx)):
        xdict[newx[i]] = i + 1
        if newx[i] in x:
            x_list.append(xdict[newx[i]])
            resx_dict[newx[i]] = y[j]
            j += 1
        elif newx[i] in insert_x:
            x_i_list.append(xdict[newx[i]])
    
    # 得到差值函数  linear: 线性插值  cubic: 三次样条插值
    Flinear = interpolate.interp1d(x_list, y, kind=kind)
    ynew = Flinear(x_i_list)
    ynew = np.array(ynew).tolist()
    ynew = [abs(round(xi, 4)) for xi in ynew]
    j = 0
    for i in x_i_list:
        k = [k for k, v in xdict.items() if v == i][0]
        resx_dict[k] = ynew[j]
        j += 1
    
    resx_dict = sorted(resx_dict.items(), key=lambda x: x[0], reverse=False)
    resx_dict = dict(resx_dict)
    print(resx_dict)



if __name__ == '__main__':
    interpolation_data(xs, ys, kind='cubic')
