import os
import time
from datetime import datetime
import re
from tkinter import *
import tkinter.messagebox
import threading
from tkinter import scrolledtext

import logging
import logging.config
CON_LOG='log.conf'
logging.config.fileConfig(CON_LOG)
logging=logging.getLogger()
from handle_main import handle

def cut_email(email):
    #切割输入的email
    email_list=re.split('[, ：; ]',email.strip())
    return email_list

def _ui():
    root=Tk()
    root.title("智能音响误唤醒测试工具")
    # root.geometry("500x300+750+200")  #窗口位置,这里四个参数分别为：宽、高、左、上
    sw = root.winfo_screenwidth()
    # print(sw)
    # 得到屏幕宽度
    sh = root.winfo_screenheight()
    # print(sh)
    # 得到屏幕高度
    ww = 100
    wh = 100
    # 窗口宽高为100
    x = (sw - ww) / 2
    y = ((sh - wh) / 5) * 4
    # root.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
    root.geometry("%dx%d+%d+%d" % (x, y, ww, wh))
    # root.minsize(560,545)
    # Label(root,text="zuopin").grid(row=0)  #使用这种方法没有办法剧中
    title = Label(root, text="              智能音响误唤醒测试工具", compound=CENTER, font=("微软雅黑", 20))
    title.grid(row=0, columnspan=3, sticky=E + W)

    def click():
        logging.info("点击开始测试按钮，开始测试")

        log_time=log_time_entry.get()
        logging.info("获取到的日志提取间隔是： "+str(log_time))

        test_time = test_time_entry.get()
        logging.info("获取到的测试总时长是： "+str(test_time))

        device_id=device_id_entry.get()
        logging.info("获取到的设备id： "+str(device_id))

        email=email_entry.get()
        logging.info("获取到的email: "+str(email))
        email_cut=cut_email(email)
        logging.info("切割后的email: "+str(email_cut))

        #添加一个线程去处理
        th=threading.Thread(target=handle,args=(text,log_time,test_time,device_id,email_cut))

        # # 添加一个线程
        # th = threading.Thread(target=I_do, args=(deviceid, email, wake_path, jiaohu_path, excel_path, device_version))
        th.setDaemon(True)  # 设置守护线程，主线程结束后，该线程也要结束
        th.start()

    log_time = StringVar()

    log_time_label = Label(root, text="日志提取间隔,单位(min) ", foreground="white", background="blue")
    log_time_label.grid(sticky=E, padx=20, pady=20)
    log_time_entry = Entry(root, textvariable=log_time, width=80)
    # e2 = Entry(root)
    log_time_entry.grid(row=1, column=1, sticky=W)

    test_time = StringVar()
    test_time_label = Label(root, text="测试时长,单位(h) ", foreground="white", background="blue")
    test_time_label.grid(sticky=E, padx=20, pady=20)
    test_time_entry = Entry(root, textvariable=test_time, width=80)
    # e2 = Entry(root)
    test_time_entry.grid(row=2, column=1, sticky=W)

    device_id = StringVar()
    device_id_label = Label(root, text="device-id ", foreground="white", background="blue")
    device_id_label.grid(sticky=E, padx=20, pady=20)
    device_id_entry = Entry(root, textvariable=device_id, width=80)
    # e2 = Entry(root)
    device_id_entry.grid(row=3, column=1, sticky=W)

    email = StringVar(value=("319910390@qq.com;"))
    email_label = Label(root, text="email ", foreground="white", background="blue")
    email_label.grid(sticky=E, padx=20, pady=20)
    email_entry = Entry(root, textvariable=email, width=80)
    # e2 = Entry(root)
    email_entry.grid(row=4, column=1, sticky=W)



    text=scrolledtext.ScrolledText(root,width=80,height=30)
    text.grid(row=5,column=1,columnspan=2,sticky=W)

    click_btn = Button(root, text="开始测试", command=click)
    click_btn.grid(row=6)

    root.mainloop()

if __name__=="__main__":
    #logging.info("xxxxxxxxxxx")
    _ui()