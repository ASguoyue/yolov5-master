import os
import random

trainval_percent = 0.2 #设置比例
train_percent = 0.8
xmlfilepath = '/home/gy/Projects/yolov4/yolov4-pytorch-master/VOCdevkit/VOC2007/Annotations'  # 修改路径
txtsavepath = '/home/gy/Projects/yolov4/yolov4-pytorch-master/VOCdevkit/VOC2007/ImageSets/Main'  #修改路径
total_xml = os.listdir(xmlfilepath)

num=len(total_xml)
list=range(num)
tv=int(num*trainval_percent)
tr=int(tv*train_percent)
trainval= random.sample(list,tv)
train=random.sample(trainval,tr)

ftrainval = open('/home/gy/Projects/yolov4/yolov4-pytorch-master/VOCdevkit/VOC2007/ImageSets/Main/trainval.txt', 'w')
ftest = open('/home/gy/Projects/yolov4/yolov4-pytorch-master/VOCdevkit/VOC2007/ImageSets/Main/test.txt', 'w')
ftrain = open('/home/gy/Projects/yolov4/yolov4-pytorch-master/VOCdevkit/VOC2007/ImageSets/Main/train.txt', 'w')
fval = open('/home/gy/Projects/yolov4/yolov4-pytorch-master/VOCdevkit/VOC2007/ImageSets/Main/val.txt', 'w')

for i  in list:
    name=total_xml[i][:-4]+'\n'
    if i in trainval:
        ftrainval.write(name)
        if i in train:
            ftrain.write(name)
        else:
            fval.write(name)
    else:
        ftest.write(name)

ftrainval.close()
ftrain.close()
fval.close()
ftest .close()
