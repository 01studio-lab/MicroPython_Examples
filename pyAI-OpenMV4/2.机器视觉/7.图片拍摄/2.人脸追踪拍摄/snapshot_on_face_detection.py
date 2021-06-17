# 人脸检测拍摄示例
#
# 提示: 本实验需要SD卡.
#
# 这个例子演示了如何在你的OpenMV摄像头上使用人脸跟踪然后拍照
#
#翻译和注释：01Studio

import sensor, image, pyb

RED_LED_PIN = 1
BLUE_LED_PIN = 3

#配置摄像头参数
sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.HQVGA) # or sensor.QQVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.

# 加载人脸检测 HaarCascade 模型. 默认使用stages=25以提高识别正确率
face_cascade = image.HaarCascade("frontalface", stages=25)

while(True):

    #红灯亮提示开始识别
    pyb.LED(RED_LED_PIN).on()
    print("About to start detecting faces...")
    sensor.skip_frames(time = 2000) # 给时间用户准备.

    #人脸检测中。
    pyb.LED(RED_LED_PIN).off()
    print("Now detecting faces!")
    pyb.LED(BLUE_LED_PIN).on()

    diff = 10 # 成功识别10次后确认为识别到人脸.

    while(diff):
        img = sensor.snapshot()
        # Threshold 和 scale 两个参数控制着识别质量和效率。具体看文档说明。
        faces = img.find_features(face_cascade, threshold=0.5, scale_factor=1.5)

        if faces:
            diff -= 1
            for r in faces:
                img.draw_rectangle(r)

    pyb.LED(BLUE_LED_PIN).off()
    print("Face detected! Saving image...")
    sensor.snapshot().save("snapshot-%d.jpg" % pyb.rng()) # 保存照片.
