'''
实验名称：FFT（快速傅里叶）运算
版本： v1.0
日期： 2019.12
实验说明：通过FFT运算，将输入的音频从时域信号转换成频域信号。通过LCD条形柱显示。
翻译和注释： 01Studio
'''
from Maix import GPIO, I2S, FFT
import image, lcd, math
from fpioa_manager import fm

#FFT参数配置
sample_rate = 38640  #采样率
sample_points = 1024 #音频采样点数
fft_points = 512  #FFT运算点数
hist_x_num = 50 #条形柱数量
x_shift = 0    #频率

#lcd初始化
lcd.init()

#麦克风初始化
fm.register(20,fm.fpioa.I2S0_IN_D0, force=True)
fm.register(19,fm.fpioa.I2S0_WS, force=True)
fm.register(18,fm.fpioa.I2S0_SCLK, force=True)

rx = I2S(I2S.DEVICE_0)
rx.channel_config(rx.CHANNEL_0, rx.RECEIVER, align_mode = I2S.STANDARD_MODE)
rx.set_sample_rate(sample_rate)

#设置LCD条形柱显示宽度
if hist_x_num > 320:
    hist_x_num = 320
hist_width = int(320 / hist_x_num) #changeable

#新建一张图片
img = image.Image()

while True:

    audio = rx.record(sample_points)   #采集音频
    fft_res = FFT.run(audio.to_bytes(),fft_points) #FFT运算
    fft_amp = FFT.amplitude(fft_res) #计算频谱幅值
    img = img.clear()
    x_shift = 0

    #计算幅值，最大为240（LCD高为240像素）
    for i in range(hist_x_num):
        if fft_amp[i] > 240:
            hist_height = 240
        else:
            hist_height = fft_amp[i]

        #计算要显示的图像，矩形实心显示。
        img = img.draw_rectangle((x_shift,240-hist_height,hist_width,hist_height),[255,255,255],2,True)
        x_shift = x_shift + hist_width

    lcd.display(img) #LCD显示
    fft_amp.clear()  #幅度值清0
