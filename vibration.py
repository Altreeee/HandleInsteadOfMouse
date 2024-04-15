'''https://blog.csdn.net/weixin_44613728/article/details/118392478'''


import ctypes

# Define necessary structures
class XINPUT_VIBRATION(ctypes.Structure):
    _fields_ = [("wLeftMotorSpeed", ctypes.c_ushort),
                ("wRightMotorSpeed", ctypes.c_ushort)]

xinput = ctypes.windll.xinput1_1  # Load Xinput.dll

# Set up function argument types and return type
XInputSetState = xinput.XInputSetState
XInputSetState.argtypes = [ctypes.c_uint, ctypes.POINTER(XINPUT_VIBRATION)]
XInputSetState.restype = ctypes.c_uint

# Now we're ready to call it.  Set left motor to 100%, right motor to 50%
# for controller 0
'''vibration = XINPUT_VIBRATION(65535, 32768)
XInputSetState(0, ctypes.byref(vibration)) # 直接调用'''


# 调用封装的函数
def set_vibration(controller, left_motor, right_motor):
    vibration = XINPUT_VIBRATION(int(left_motor * 65535), int(right_motor * 65535))
    XInputSetState(controller, ctypes.byref(vibration))

#set_vibration(0, 1.0, 0.5)   #参数分别为： 控制器编号（默认为0）  左马达震动系数   右马达震动系数
