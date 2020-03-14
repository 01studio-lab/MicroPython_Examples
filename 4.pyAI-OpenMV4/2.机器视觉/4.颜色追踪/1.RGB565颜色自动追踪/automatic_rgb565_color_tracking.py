# RGB565彩色自动追踪
#
# 本例程展示了单个颜色追踪.
#
#翻译：01Studio

import sensor, image, time
print("Letting auto algorithms run. Don't put anything in front of the camera!")

#摄像头初始化
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # 颜色追踪必须关闭摄像头的自动增益
sensor.set_auto_whitebal(False) # 颜色追踪必须关闭自动白平衡
clock = time.clock()

#捕获摄像头中心区域的颜色阈值. 50*50中心区域
r = [(320//2)-(50//2), (240//2)-(50//2), 50, 50]

#将需要识别的颜色放在摄像头中心
print("Auto algorithms done. Hold the object you want to track in front of the camera in the box.")
print("MAKE SURE THE COLOR OF THE OBJECT YOU WANT TO TRACK IS FULLY ENCLOSED BY THE BOX!")
for i in range(60):
    img = sensor.snapshot()
    img.draw_rectangle(r)

print("Learning thresholds...")
threshold = [50, 50, 0, 0, 0, 0] # Middle L, A, B values.
for i in range(60):
    img = sensor.snapshot()
    hist = img.get_histogram(roi=r)
    lo = hist.get_percentile(0.01) #  获取1％范围的直方图的CDF（根据需要调整）!
    hi = hist.get_percentile(0.99) #  获取99％范围的直方图的CDF（根据需要调整）!
    # 百分位数平均值.
    threshold[0] = (threshold[0] + lo.l_value()) // 2
    threshold[1] = (threshold[1] + hi.l_value()) // 2
    threshold[2] = (threshold[2] + lo.a_value()) // 2
    threshold[3] = (threshold[3] + hi.a_value()) // 2
    threshold[4] = (threshold[4] + lo.b_value()) // 2
    threshold[5] = (threshold[5] + hi.b_value()) // 2
    for blob in img.find_blobs([threshold], pixels_threshold=100, area_threshold=100, merge=True, margin=10):
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        img.draw_rectangle(r)

print("Thresholds learned...")
print("Tracking colors...")

while(True):
    clock.tick()
    img = sensor.snapshot()

    #跟学习到的色块LAB模型[Threshold]做对比
    for blob in img.find_blobs([threshold], pixels_threshold=100, area_threshold=100, merge=True, margin=10):
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
    print(clock.fps())
