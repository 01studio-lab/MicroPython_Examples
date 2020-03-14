# 普通拍照例程
#
# 提示: 你需要插入SD卡来运行这个例程.
#
# 你可以使用你的OpenMV设备保存图片。

#导入相关模块，pyb用于LED控制。
import sensor, image, pyb

RED_LED_PIN = 1
BLUE_LED_PIN = 3

#摄像头相关初始化
sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QVGA) # or sensor.QQVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.

#红灯亮提示拍照开始
pyb.LED(RED_LED_PIN).on()
sensor.skip_frames(time = 2000) # 给2秒时间用户准备.

pyb.LED(RED_LED_PIN).off()

#蓝灯亮提示正在拍照
pyb.LED(BLUE_LED_PIN).on()

print("You're on camera!")
sensor.snapshot().save("example.jpg") # 拍摄并保存相关文件，也可以用"example.bmp"或其它。

pyb.LED(BLUE_LED_PIN).off() #提示拍照完成
print("Done! Reset the camera to see the saved image.")
