###自己编写工具
import os
import os.path
from xml.etree.ElementTree import parse, Element

# .xml文件地址
path = "/home/gy/DATA/SAR_ship/Annotations/"
# 得到文件夹下所有文件名称
files = os.listdir(path)
s = []
# 遍历文件夹
for xmlFile in files:
    # 判断是否是文件夹,不是文件夹才打开
    if not os.path.isdir(xmlFile):
        print(xmlFile)
        pass
    path = "/home/gy/DATA/SAR_ship/Annotations/"
    newStr = os.path.join(path, xmlFile)
    #最核心的部分,路径拼接,输入的是具体路径
    #得到.xml文件的根（也就是annotation）
    dom = parse(newStr)
    root = dom.getroot()
    #获得后缀.前的文件名(分离文件名和扩展名)
    part = os.path.splitext(xmlFile)[0]
    # 文件名+后缀
    part1 = part + '.jpg'
    # path里的新属性值：
    newStr1 = '/home/gy/DATA/SAR_ship/JPEGImages/' + part1
    #通过句柄找到path的子节点，然后给子节点设置内容
    root.find('path').text = newStr1
    # #打印输出
    print('已经修改')
    dom.write(newStr, xml_declaration=True)
    pass