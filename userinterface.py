from  PyQt6.QtWidgets import (QWidget,QDockWidget, QSpacerItem,QHBoxLayout,QLabel, QMainWindow,QApplication,QVBoxLayout,QWidget,QPushButton)
from PyQt6.QtCore import Qt,QSize
from PyQt6.QtGui import QPalette,QColor,QPixmap
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
        
        #the bellow are commented out for testing purposes
        #self.finishpom=QPushButton("Finish")
        #self.finishpom.clicked.connect(self.finish_pom)
        
        #central widget init
        self.timer_widget=QWidget()
        self.setCentralWidget(self.timer_widget)

        #layout init
        self.mlayout=QVBoxLayout()
        self.mlayout.addWidget(self.timerlabel)
        self.mlayout.addWidget(self.startbutton)
        #the bellow line is commented out, it's for testing
        #self.mlayout.addWidget(self.finishpom)
        self.mlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_widget.setLayout(self.mlayout)

        #Dock init, TODO: add a style to the docker so it doesn't look so similar
        #to the rest of the app
        self.dockarea=QDockWidget(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea,self.dockarea)
        #Dock main widget and layout
        self.pompom_tracker=QWidget(self)
        pompom_layout=QVBoxLayout()
        pompom_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.pompom_tracker.setLayout(pompom_layout)
        self.dockarea.setWidget(self.pompom_tracker)

        ##dock widgets
        self.pompom_lab=QLabel('Pompommeter')
        self.pompommeter=QWidget(self.dockarea)
        self.ppm_layout=QHBoxLayout(self.pompommeter)
        self.pompommeter.setLayout(self.ppm_layout)
        ##widget addition
        pompom_layout.addWidget(self.pompom_lab)
        pompom_layout.addWidget(self.pompommeter)
        ##widget props
        self.pompoms_earned=[]




        
        self.th_init()
 
    def begin_timer(self):
        #print(f"Timer is alive:{self.timer_thread.is_alive()}")
        start_time=time.time()
        cur_time=time.time()
        while cur_time-start_time != pompom_utils.max_time:
                cur_time=time.time()
                self.ms,self.s,self.m,self.h=pompom_utils.timer_format(cur_time-start_time)
                #print(f"{self.h}:{self.m}:{self.s}:{self.ms}")
        
        self.startbutton.setDisabled(False)
        self.lhour+=self.h
        self.lmin+=self.m

        #earn a pompom for a pomodoro completed, this is more for the fun of it
        pom=QPixmap('491481_small.png')
        pompom=QLabel().setPixmap(pom)
        self.pompoms_earned.append(pompom)

        #if 4 pom poms are earned, reset
        #TODO:after 4 pompoms the app should begin a long break
        if len(self.pompoms_earned)>4:
             for i in self.pompoms_earned:
                  self.ppm_layout.removeWidget(i)
        else:
            self.ppm_layout.addWidget(pompom)
        
    #TEST FUNCTION
    def finish_pom(self):
         pompom=QLabel()
         pom=QPixmap("491481_small.png")
         pom.scaledToHeight(32)
         pom.scaledToWidth(32)
         pompom.setPixmap(pom)
         self.ppm_layout.addWidget(pompom)

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
            #TODO: Figure out how to make the self.ms display neater
            self.timerlabel.setText(time.strftime(disp_f[0],ctim)+disp_f[1]+f"{self.ms}")
            #self.timerlabel.setText(f"{self.h}:{self.m}:{self.s}:{self.ms}")

    def th_init(self):
        self.timer_thread=th.Thread(target=self.begin_timer,name='Timer')
        self.ui_update_thread=th.Thread(target=self.update_ui,name='UI Messenger')

    def thread_activate(self):
         self.timer_thread.start()
         self.ui_update_thread.start()
         self.startbutton.setDisabled(True)


if __name__=="__main__":
    pompom=QApplication([])
    time_app=mwindow()
    time_app.show()
    pompom.exec()