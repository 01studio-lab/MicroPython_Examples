#通过特征点识别对象例程
#
#给摄像头展示一个对象，然后运行程序，程序将提取一组特征点。
#提取完成后将将自动跟踪设备对象。如果需要重新识别请重新运行程序。
#注意：可以在文档中查看find_keypoints 和 match_keypoints 两个调优参数。
#
#翻译：01Studio

import sensor, time, image

# 重启摄像头
sensor.reset()

# 摄像头初始化配置
sensor.set_contrast(3)
sensor.set_gainceiling(16)
sensor.set_framesize(sensor.VGA)
sensor.set_windowing((320, 240))
sensor.set_pixformat(sensor.GRAYSCALE)

sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False, value=100)

def draw_keypoints(img, kpts):
    if kpts:
        print(kpts)
        img.draw_keypoints(kpts)
        img = sensor.snapshot()
        time.sleep(1000)

kpts1 = None
# 提示: 也可以使用下面语句从文件导入特征点。
#kpts1 = image.load_descriptor("/desc.orb")
#img = sensor.snapshot()
#draw_keypoints(img, kpts1)

clock = time.clock()

while (True):

    clock.tick()
    img = sensor.snapshot()
    if (kpts1 == None):
        # 提示: 默认情况下 find_keypoints 会返回多种尺寸的特征点，识别灵活。
        kpts1 = img.find_keypoints(max_keypoints=150, threshold=10, scale_factor=1.2)
        draw_keypoints(img, kpts1)

    else:
        # 提示: 当提取关键字以匹配第一个描述符时，我们使用normalization =True 方式来提取
        # 关键点只来自第一个刻度，它将匹配第一个描述符中的一个刻度。
        kpts2 = img.find_keypoints(max_keypoints=150, threshold=10, normalized=True)
        if (kpts2):
            match = image.match_descriptor(kpts1, kpts2, threshold=85)
            if (match.count()>10):
                # >10判断为特征点一致。用户可以自行调整
                # 画圆和交叉用于展示特征点.
                img.draw_rectangle(match.rect())
                img.draw_cross(match.cx(), match.cy(), size=10)

            print(kpts2, "matched:%d dt:%d"%(match.count(), match.theta()))
            # 提示: 如果你想绘制观点的，请取消下一行语句的注释
            #img.draw_keypoints(kpts2, size=KEYPOINTS_SIZE, matched=True)

    # Draw FPS
    img.draw_string(0, 0, "FPS:%.2f"%(clock.fps()))
