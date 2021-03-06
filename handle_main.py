from tkinter import *
import os
import time
import datetime
import logging
import logging.config
CON_LOG='log.conf'
logging.config.fileConfig(CON_LOG)
logging=logging.getLogger()
from public import load_log,log_check,clear_result,save_result,load_audio,delete_files
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

    time_span=0

    logging.info("首先先记录下开始时间为： "+str(data1))
    # global first_flag
    first_flag=True
    logging.info("先删除日志文件")
    delete_files()
    try:
        # logging.info("先删除日志文件")
        # delete_files()
        while True:

            t11 = time.localtime()  # <class 'time.struct_time'>
            data11 = time.strftime('%Y-%m-%d %H:%M:%S', t11)  # str
            # print(data1)
            # print(type(data1))
            data11 = datetime.datetime.strptime(data11, '%Y-%m-%d %H:%M:%S')
            logging.info("当前循环开始时间为： "+str(data11))



            if first_flag:
                text.insert(END, "首次拉取日志和audio文件并处理\n")
                logging.info("首先要提取下当前日志，为了最后过滤")
                filepath = load_log(device_id)
                logging.info("开始拉取audio文件")
                audiopath = load_audio(device_id, first_flag)
                logging.info("拉取audio文件结束")
                logging.info("开始正则匹配")
                log_check(text, filepath, first_flag)
                first_flag=False

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

            # dd2=data2-data11
            # logging.info("本次循环耗时： "+str(dd2))
            # time_span=time_span+dd2
            # logging.info("循环总共耗时： "+str(time_span))

            logging.info("判断时间间隔是否超过了要测试的时间")
            logging.info("test_time:  "+str(test_time))
            logging.info("time_interval: "+str(time_interval))
            logging.info("time_span: "+str(time_span))

            if time_interval>test_time or time_span>test_time:
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
                text.insert(END, "提取日志，并转码\n")
                filepath=load_log(device_id)  #返回的是转码之后的log,直接可以执行正则了
                logging.info("开始拉取audio文件")
                text.insert(END,"拉取audio文件\n")
                audiopath=load_audio(device_id,first_flag)
                logging.info("拉取audio文件结束")
                logging.info("开始正则匹配")
                log_check(text,filepath,first_flag)
                first_flag=False

                t22=time.localtime()
                #time.strftime('%Y-%m-%d %H:%M:%S', t2)
                data22=time.strftime('%Y-%m-%d %H:%M:%S',t22)
                data22=datetime.datetime.strptime(data22,'%Y-%m-%d %H:%M:%S')
                logging.info("当前循环结束时间为:  "+str(data22))

                d22=data22-data11
                d22_second=d22.seconds
                logging.info("本次循环时间间隔为: "+str(d22_second))
                time_span=time_span+d22_second

    except Exception as e:
        logging.error("异常信息： "+str(e))
        logging.error("出现了异常，开始保存文件")
        text.insert(END,"出现了异常,开始处理已保存文本\n")
        result_path=save_result()
        if result_path==None:
            logging.info("没有唤醒文件")
            my_send_email(email,result_path,test_time_h)

        else:
            #存在唤醒文件
            new_result_path=clear_result()
            my_send_email(email,new_result_path,test_time_h)

        text.insert(END, '测试结束')
    else:
        result_path = save_result()
        if result_path == None:
            logging.info("没有唤醒文件")
            my_send_email(email, result_path, test_time_h)

        else:
            # 存在唤醒文件
            logging.info("有唤醒文件")
            new_result_path = clear_result()
            my_send_email(email, new_result_path, test_time_h)

        text.insert(END, '测试结束')




if __name__=='__main__':
    # # t1 = time.localtime()  # <class 'time.struct_time'>
    # # data1 = time.strftime('%Y-%m-%d %H:%M:%S', t1)  # str
    # # print(data1)
    # # print(type(data1))
    # # data1=datetime.datetime.strptime(data1,'%Y-%m-%d %H:%M:%S')
    # # print(data1)
    # # print(type(data1))
    # #
    # # time.sleep(10)
    # # t2 = time.localtime()
    # # data2=time.strftime('%Y-%m-%d %H:%M:%S', t2)
    # # print(data2)
    # # print(type(data2))
    # # data2 = datetime.datetime.strptime(data2, '%Y-%m-%d %H:%M:%S')
    # # print(data2)
    # # print(type(data2))
    # #
    # # d=data2-data1
    # #
    # # print(d.seconds)
    #
    # t1 = time.localtime()  # <class 'time.struct_time'>
    # data1 = time.strftime('%Y-%m-%d %H:%M:%S', t1)  # str
    # # print(data1)
    # # print(type(data1))
    # data1 = datetime.datetime.strptime(data1, '%Y-%m-%d %H:%M:%S')
    # # print(data1)
    # # print(type(data1))
    #
    # logging.info("首先先记录下开始时间为： " + str(data1))
    #
    # time.sleep(4)
    #
    # t2 = time.localtime()
    # data2 = time.strftime('%Y-%m-%d %H:%M:%S', t2)
    # # print(data2)
    # # print(type(data2))
    # data2 = datetime.datetime.strptime(data2, '%Y-%m-%d %H:%M:%S')
    # # print(data2)
    # # print(type(data2))
    # logging.info("记录下当前时间为： " + str(data2))
    #
    #
    # d=data2-data1
    # print("d: ",d)
    # time_interval=d.seconds
    # logging.info("时间间隔为(s): "+str(time_interval))

    num=10
    num1=9
    num2=12

    if num1>num or num2>num:
        print("执行了")
    else:
        print("没有执行")

