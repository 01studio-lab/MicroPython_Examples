#实验名称：物品检测
#翻译和注释：01Studio
#实验目的：使用20class模型识别20种物体

import sensor,image,lcd,time
import KPU as kpu

#摄像头初始化
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)  #摄像头后置方式

lcd.init() #LCD初始化

clock = time.clock()

#模型分类，按照20class顺序
classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']

#下面语句需要将模型（20class.kfpkg）烧写到flash的 0x500000 位置
#task = kpu.load(0x500000)

#将模型放在SD卡中。
task = kpu.load("/sd/20class.kmodel") #模型SD卡上

#网络参数
anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)

#初始化yolo2网络，识别可信概率为0.7（70%）
a = kpu.init_yolo2(task, 0.7, 0.3, 5, anchor)

while(True):

    clock.tick()

    img = sensor.snapshot()
    code = kpu.run_yolo2(task, img) #运行yolo2网络


    if code:
        for i in code:
            a=img.draw_rectangle(i.rect())
            a = lcd.display(img)

            lcd.draw_string(i.x(), i.y(), classes[i.classid()], lcd.RED, lcd.WHITE)
            lcd.draw_string(i.x(), i.y()+12, '%f1.3'%i.value(), lcd.RED, lcd.WHITE)
    else:
        a = lcd.display(img)

    print(clock.fps())#打印FPS
