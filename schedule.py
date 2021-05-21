import time
import FG_trade_min

# 定时程序，思路就是通过将延迟函数使用递归完成周期启动的效果；
import threading
import time

# 参数, inc, 为每次间隔的秒数
# 调用或者说循环的函数为
def fun_timer(inc):
    print('try to link Wind, after 6hours try again')
    global timer
    
    timer = threading.Timer(inc, fun_timer, (inc,))
    FG_trade_min.runFunc()
    timer.start()
    
# .5秒后开始触发,# 每隔1秒
#timer = threading.Timer(.5, fun_timer, (1,))
#timer.start()

fun_timer(21600);

# 15秒后停止定时器
time.sleep(259200);

#cancel停止定时器的工作
print('over')
timer.cancel()