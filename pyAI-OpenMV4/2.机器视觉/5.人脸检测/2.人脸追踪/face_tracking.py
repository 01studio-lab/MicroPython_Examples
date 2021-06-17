# 人脸追踪例程
#
# 这个例程展示了如何使用关键特征来追踪一个已经使用Haar Cascade检测出来的人脸。
# 程序第一阶段先使用 Haar Cascade 找出人脸.然后使用关键特征来学习，最后不停的找这个人脸。
# 关键特征点可以用来追踪任何栋。
#
#翻译：01Studio

import sensor, time, image

# Reset sensor
sensor.reset()
sensor.set_contrast(3)
sensor.set_gainceiling(16)
sensor.set_framesize(sensor.VGA)
sensor.set_windowing((320, 240)) #在VGA（640*480）下开个小窗口，相当于数码缩放。
sensor.set_pixformat(sensor.GRAYSCALE)

# 延时以便摄像头稳定工作
sensor.skip_frames(time = 2000)

# 加载 Haar Cascade 模型
# 默认使用25个步骤，减少步骤会加快速度但会影响识别成功率.
face_cascade = image.HaarCascade("frontalface", stages=25)
print(face_cascade)

# 特征kpts1
kpts1 = None

# 找到人脸!
while (kpts1 == None):
    img = sensor.snapshot()
    img.draw_string(0, 0, "Looking for a face...")
    # Find faces
    objects = img.find_features(face_cascade, threshold=0.5, scale=1.25)
    if objects:
        # 将 ROI（x,y,w,h）往各个方向扩展 31 像素
        face = (objects[0][0]-31, objects[0][1]-31,objects[0][2]+31*2, objects[0][3]+31*2)
        # 使用扩展后的 ROI 区域（人脸）学习关键点
        kpts1 = img.find_keypoints(threshold=10, scale_factor=1.1, max_keypoints=100, roi=face)
        # 用矩形框展示人脸
        img.draw_rectangle(objects[0])

# 打印关键点
print(kpts1)
img.draw_keypoints(kpts1, size=24)
img = sensor.snapshot()
time.sleep(2000) #暂停以便观察特征

# FPS clock
clock = time.clock()

while (True):
    clock.tick()
    img = sensor.snapshot()
    # 从图像中提取关键点
    kpts2 = img.find_keypoints(threshold=10, scale_factor=1.1, max_keypoints=100, normalized=True)

    if (kpts2):
        # 跟关键点kpts1匹配
        c=image.match_descriptor(kpts1, kpts2, threshold=85)
        match = c[6] # C[6] 为 matches值，这个值越大表示匹配程度越高.
        if (match>5): #设置当大于5的时候为匹配成功，并画图标示。打印相关信息。
            img.draw_rectangle(c[2:6])
            img.draw_cross(c[0], c[1], size=10)
            print(kpts2, "matched:%d dt:%d"%(match, c[7]))

    # Draw FPS
    img.draw_string(0, 0, "FPS:%.2f"%(clock.fps()))
