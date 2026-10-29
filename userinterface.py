from  PyQt6.QtWidgets import (QWidget,QDockWidget, QHeaderView,QLabel, QMainWindow,QApplication,QVBoxLayout,QWidget,QPushButton)
from PyQt6.QtCore import Qt,QSize
import threading as th
import time
import pompom_utils
import sys

class mwindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.lhour=0
        self.lmin=0
        self.lsec=0
        self.lmsec=0
        
        #widgets
        self.timerlabel=QLabel("00:00:00")
        self.timerlabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.startbutton=QPushButton("Begin Timer")
        self.startbutton.clicked.connect(self.thread_activate)

        #dock
        self.dockarea=QDockWidget(self)
        self.pompom_tracker=QWidget(self)
        self.pompom_layout=QVBoxLayout(self)
        self.pompom_tracker.setLayout(self.pompom_layout)



        #central widget init
        self.timer_widget=QWidget()
        self.setCentralWidget(self.timer_widget)

        #layout init
        self.mlayout=QVBoxLayout()
        self.mlayout.addWidget(self.timerlabel)
        self.mlayout.addWidget(self.startbutton)
        self.mlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_widget.setLayout(self.mlayout)
        
        self.th_init()


    
    def begin_timer(self):
        #print(f"Timer is alive:{self.timer_thread.is_alive()}")
        start_time=time.time()
        cur_time=time.time()
        while cur_time-start_time != pompom_utils.max_time:
                cur_time=time.time()
                self.ms,self.s,self.m,self.h=pompom_utils.timer_format(cur_time-start_time)
                #print(f"{self.h}:{self.m}:{self.s}:{self.ms}")
        
        self.lhour+=self.h
        self.lmin+=self.m

    def update_ui(self):
        
        formating={
             (True,False):["%M:%S",f".0"],
             (True,True):["%M:%S",f"."],
             (False,False):["%H:%M:%S",f".0"],
             (False,True):["%H:%M:%S",f"."]
        }
        while self.timer_thread.is_alive():
            #print(f"timer_thred alive:{self.timer_thread.is_alive()}")
            disp_f=formating[(self.h==0,self.ms>=10)]
            ctim=time.struct_time([0,0,0,self.h,self.m,self.s,0,0,0])
            self.timerlabel.setText(time.strftime(disp_f[0],ctim)+disp_f[1]+f"{self.ms}")
            #self.timerlabel.setText(f"{self.h}:{self.m}:{self.s}:{self.ms}")

    def th_init(self):
        self.timer_thread=th.Thread(target=self.begin_timer,name='Timer')
        self.ui_update_thread=th.Thread(target=self.update_ui,name='UI Messenger')

    def thread_activate(self):
         self.timer_thread.start()
         self.ui_update_thread.start()


if __name__=="__main__":
    pompom=QApplication([])
    time_app=mwindow()
    time_app.show()
    pompom.exec()