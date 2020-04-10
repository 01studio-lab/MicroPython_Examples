#  低功耗蓝牙模块（BLE Module）

说明：模块厂商 WeBee，型号：TLS-02
出厂参数：广播名称：BLE SPS; 波特率：9600; 广播间隔：100ms

## 构造对象
` ` `
from tls02 import TLS02
BLE= TLS02(3,9600)
` ` `

## 使用方法
### 查看广播名字
` ` `
BLE.Name_Check()
` ` `
### 设置广播名字
` ` `
BLE.Name_Set("01Studio") #设置成01Studio
` ` `

### 查看广播间隔,单位ms
` ` `
BLE.BI_Check()
` ` `
### 设置广播间隔,单位ms
` ` `
BLE.BI_Set(200)
` ` `

### 查看波特率
` ` `
BLE.Baudrate_Check()
` ` `
### 设置波特率
` ` `
BLE.Baudrate_Set(9600) #设置完成后需要复位，以及重置开发板UART波特率
` ` `
### 模块复位
` ` `
BLE.RST()   #复位后需要延时600ms等待重新启动
` ` `

### 模块重置，恢复出厂设置
` ` `
BLE.RESET()   #模块重置后会自动复位，复位后需要延时600ms等待重新启动
` ` `

