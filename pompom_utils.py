import math 
import time

max_time=1500
rest_time=300

def timer_format(time_s):
    msec=math.trunc(time_s*100)%100
    sec=math.trunc(time_s)%60
    min=math.trunc(time_s/60)%60
    hr=math.trunc(time_s/3600)

    return (msec,sec,min,hr)

#def ui_start_timer():


def _prt_start_timer():
    start_time=time.time()
    cur_time=start_time

    while cur_time-start_time != max_time:
        cur_time=time.time()
        ms,s,m,h=timer_format(cur_time-start_time)
        print(f"{h}:{m}:{s}:{ms}")
    
    return h,m,s,ms

if __name__=='__main__':
    _prt_start_timer()