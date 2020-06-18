#视频录制示例
#
# 提示: 你需要插入SD卡来运行此程序.
#
#翻译和注释：01Studio

import video, sensor, image, lcd, time

#摄像头初始化
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)   #后置拍摄模式
sensor.skip_frames(30)

#LCD初始化
lcd.init()

#指定录制文件路径和文件名
v = video.open("/sd/example.avi", record=1,interval=100000, quality=50)

i = 0  #计算录制帧数

while True:

    tim = time.ticks_ms()
    img = sensor.snapshot()

    lcd.display(img)
    img_len = v.record(img) #img_len为返回的录制帧长度。

    print("record",time.ticks_ms() - tim) #打印录制的每帧间隔

    #录制100帧,每帧默认100ms，即10秒视频。
    i += 1
    if i >50:
        break

v.record_finish() #停止录制
print("finish") #录制完成提示
