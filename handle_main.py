from tkinter import *
import os
import time
import datetime
import logging
import logging.config
CON_LOG='log.conf'
logging.config.fileConfig(CON_LOG)
logging=logging.getLogger()
from public import load_log,log_check,clear_result,save_result
from send_email import my_send_email
def handle(text,log_time,test_time,device_id,email):
    #clear_result()
    # print("handle接受到的log_time（分钟）: ",log_time)
    # print("Handle接受到的test_tiem(小时):",test_time)
    # print("handle接收到的device_id： ",device_id)
    test_time_h=str(test_time)
    logging.info("开始处理")
    logging.info("handle接收到的log_time(分钟)："+str(log_time))
    logging.info("handle接收到的test_time(h):"+str(test_time))
    logging.info("handle接收到的device_id： "+str(device_id))
    logging.info("handle接收到的email: "+str(email))
    log_time=int(log_time)*60
    logging.info("log_time分钟转换为秒： "+str(log_time))
    test_time=float(test_time)*60*60
    logging.info("test_time小时转换为秒： "+str(test_time))

    t1 = time.localtime()  # <class 'time.struct_time'>
    data1 = time.strftime('%Y-%m-%d %H:%M:%S', t1)  # str
    # print(data1)
    # print(type(data1))
    data1 = datetime.datetime.strptime(data1, '%Y-%m-%d %H:%M:%S')
    # print(data1)
    # print(type(data1))

    logging.info("首先先记录下开始时间为： "+str(data1))

    while True:
        logging.info("循环执行")
        t2 = time.localtime()
        data2 = time.strftime('%Y-%m-%d %H:%M:%S', t2)
        # print(data2)
        # print(type(data2))
        data2 = datetime.datetime.strptime(data2, '%Y-%m-%d %H:%M:%S')
        # print(data2)
        # print(type(data2))
        logging.info("记录下当前时间为： "+str(data2))
        d=data2-data1
        time_interval=d.seconds
        logging.info("时间间隔为(s): "+str(time_interval))

        logging.info("判断时间间隔是否超过了要测试的时间")

        if time_interval>test_time:
            logging.info("时间间隔超过了要测试的时间，退出循环")
            break
        else:
            logging.info("时间间隔没有超过要测试的时间，等待日志时间后，接着执行")
            text.insert(END,"时间间隔没有超过要测试的时间，等待日志时间后，接着执行\n")
            #time.sleep(log_time)
            for i in range(int(log_time/10)):
                logging.info("等待......"+str(i))
                time.sleep(10)
            logging.info("等待时间结束")
            logging.info("提取日志，并转码")
            filepath=load_log(device_id)  #返回的是转码之后的log,直接可以执行正则了

            logging.info("开始正则匹配")
            log_check(text,filepath)

    result_path=save_result()
    if result_path==None:
        logging.info("没有唤醒文件")
        my_send_email(email,result_path,test_time_h)

    else:
        #存在唤醒文件
        new_result_path=clear_result()
        my_send_email(email,new_result_path,test_time_h)

    text.insert(END, '测试结束')

    #
    # for i in range(5):
    #     filepath=load_log(device_id)
    #     tmp1="This is "+str(i)
    #     text.insert(END, tmp1)
    #     text.insert(END,'\n')
    #     text.see(END)
    #     logging.info("等待...............")
    #     time.sleep(20)
    #     #load_log返回的路径就是已经转换格式的日志路径，可以正则了
    #     #正则
    #     log_check(text,filepath)
    #
    # text.insert(END,'测试结束')


if __name__=='__main__':
    t1 = time.localtime()  # <class 'time.struct_time'>
    data1 = time.strftime('%Y-%m-%d %H:%M:%S', t1)  # str
    print(data1)
    print(type(data1))
    data1=datetime.datetime.strptime(data1,'%Y-%m-%d %H:%M:%S')
    print(data1)
    print(type(data1))

    time.sleep(10)
    t2 = time.localtime()
    data2=time.strftime('%Y-%m-%d %H:%M:%S', t2)
    print(data2)
    print(type(data2))
    data2 = datetime.datetime.strptime(data2, '%Y-%m-%d %H:%M:%S')
    print(data2)
    print(type(data2))

    d=data2-data1

    print(d.seconds)


