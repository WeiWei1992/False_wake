import os
import logging
import logging.config
CON_LOG='log.conf'
logging.config.fileConfig(CON_LOG)
logging=logging.getLogger()
import time
from datetime import datetime
import re
from tkinter import *
import shutil
def conver_log(pathfile1,pathfile2):
    #转换日志格式，要不然无法正则
    lineNumbers = 0
    with open(pathfile1,'rb') as f:
        while True:
            try:
                line = f.readline()
                lineNumbers=lineNumbers+1
                if not line:
                    logging.info("日志转换到了结尾")
                    break
            except UnicodeDecodeError:
                logging.error("出现了编码错误")
                logging.error("出现错误的行是:  "+str(lineNumbers))
            else:
                line = line.decode('utf-8', 'ignore')  #转换编码格式
                save_txt(line, pathfile2)


def save_txt(line, pathfile):
    # print("保存txt: ",line,filter_log_path)
    if pathfile == None:
        logging.error("保存结果的文件路径是空，请检查")
        return None
    try:
        # print("保存路径...",pathfile)
        with open(pathfile, 'a', encoding='utf-8') as f:
            f.write(line)
            #f.write('\n')
    except:
        # print("文件写入错误")
        logging.error("文件写入错误")
        return None
    else:
        return pathfile


def load_audio(device_id,first_flag):
    # dt=datetime.now()
    # now_time = dt.strftime('%Y_%m_%d_%H_%M_%S')
    my_path = os.path.abspath(os.getcwd())
    audio_path=my_path + '/Logs/audio/audio_%s' % (now_time)

    if first_flag:
        audio_path_first = my_path + '/Logs/audio/audio_first_%s' % (now_time)
        if device_id:
            adbshell='adb -s ' + str(device_id) + ' pull /tmp/audio ' + audio_path_first
        else:
            adbshell = 'adb pull /tmp/audio ' + audio_path_first
        logging.info("拉取audio文件命令: "+str(adbshell))
        res=os.path.exists(audio_path_first)
        if res:
            logging.info("文件路径存在,直接拉取")
            os.system(adbshell)
        else:
            logging.info("文件不存在，新建文件夹")
            os.mkdir(audio_path_first)
            os.system(adbshell)
        time.sleep(3)
    else:
        if device_id:
            adbshell='adb -s ' + str(device_id) + ' pull /tmp/audio ' + audio_path
        else:
            adbshell = 'adb pull /tmp/audio ' + audio_path
        logging.info("拉取audio文件命令: "+str(adbshell))
        res=os.path.exists(audio_path)
        if res:
            logging.info("文件路径存在,直接拉取")
            os.system(adbshell)
        else:
            logging.info("文件不存在，新建文件夹")
            os.mkdir(audio_path)
            os.system(adbshell)
        time.sleep(3)
        return audio_path


def load_log(device_id=None, filepath=None):
    filepath=None
    dt = datetime.now()
    global now_time
    now_time = dt.strftime('%Y_%m_%d_%H_%M_%S')  # 得用下划线，用： 号无法截图保存
    # global my_path

    my_path = os.path.abspath(os.getcwd())
    if filepath == None:
        filepath = my_path + '/Logs/original_log/uai_log_%s' % (now_time)
        resultpath=my_path + '/Logs/result_log/uai_result_log_%s' % (now_time)
    if device_id :
        adbshell = 'adb -s ' + str(device_id) + ' pull /data/uai_log.txt ' + filepath
        #adbshell = 'adb pull /tmp/uai_log.txt ' + filepath
    else:
        adbshell = 'adb pull /data/uai_log.txt ' + filepath
    logging.info("adb shell 命令：" + adbshell)
    result = os.path.exists(filepath)
    if result:  # 如果该文件夹存在
        os.system(adbshell)
    else:  # 如果不存在，先新建
        os.mkdir(filepath)
        os.system(adbshell)

    result_log=os.path.exists(resultpath)
    if result_log:
        pass
    else:
        os.mkdir(resultpath)

    filepath_log=filepath+'\\uai_log.txt'
    result_log_path=resultpath+'\\uai_log_convert.txt'


    file_path_1 = filepath + '\\uai_log.txt'
    file_path_2 = resultpath + '\\uai_log_convert.txt'

    time.sleep(3)
    print("file_path_1:  ",file_path_1 )
    print("file_path_2:  ",file_path_2)
    logging.info("file_path_1: "+str(file_path_1))
    logging.info("file_path_2: "+str(file_path_2))

    #2020-08-24新增，使用的过程中，出现了一次拉取出来的日志是空，转换后的路径是空，导致异常，可以在日志中加入一行无关紧要的日志。
    tmp_txt='this is conver log ,because of if the log is none,the program will be error,so I add this line ---weiwei \n\n'
    save_txt(tmp_txt,file_path_2)

    conver_log(file_path_1,file_path_2)
    return file_path_2
    #return file_path_1,file_path_2


res = os.getcwd()
result_tmp_path = os.path.join(res, 'Logs/result_tmp.txt')
result_tmp_path_1 = os.path.join(res, 'Logs/result_tmp_1.txt')
result_path=os.path.join(res,'Logs/result.txt')

def delete_files():
    logging.info("首先清除下日志文件")
    audio_path=os.path.join(res,'Logs/audio')
    print(audio_path)
    del_list_audio=os.listdir(audio_path)
    #print("del_list_audio: ",del_list_audio)

    original_log_path=os.path.join(res,'Logs/original_log')
    del_original=os.listdir(original_log_path)

    result_history_path=os.path.join(res,'Logs/result_history')
    del_result_history=os.listdir(result_history_path)

    result_log_path=os.path.join(res,'Logs/result_log')
    def_result_log=os.listdir(result_log_path)

    # del_list=[]
    # del_list.append(del_list_audio)
    # del_list.append(del_original)
    # del_list.append(del_result_history)
    # del_list.append(def_result_log)

    for f in del_list_audio:
        logging.info("删除: "+str(audio_path))
        #print("f: ",f)
        file_path=os.path.join(audio_path,f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    for f in del_original:
        #print("f: ",f)
        logging.info("删除： "+str(original_log_path))
        file_path=os.path.join(original_log_path,f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    for f in del_result_history:
        #print("f: ",f)
        logging.info("删除： "+str(result_history_path))
        file_path=os.path.join(result_history_path,f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    for f in def_result_log:
        #print("f: ",f)
        logging.info("删除： "+str(result_log_path))
        file_path=os.path.join(result_log_path,f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    result_tmp_1_path=os.path.join(res,'Logs/result_tmp_1.txt')
    #result_tmp_path_1
    # print("res: ",res)
    # print("result_tmp_path_1:",result_tmp_path_1)
    # print("result_tmp_1_path",result_tmp_1_path)
    if os.path.isfile(result_tmp_1_path):
        logging.info("删除： "+str(result_tmp_1_path))
        os.remove(result_tmp_1_path)

    # for f in audio_path:
    #     print("f:",f)
    #     file_path=os.path.join(audio_path,f)
    #     print("file_path: ",file_path)
    #     if os.path.isfile(file_path):
    #         os.remove(file_path)
    #     elif os.path.isdir(file_path):
    #         shutil.rmtree(file_path)


def clear_result():
    now=time.time()
    #print(now)
    timeArray=time.localtime(now)
    #print(timeArray)
    my_now=time.strftime("%Y_%m_%d_%H_%M_%S",timeArray)
    #print(my_now)
    #res = os.getcwd()
    #result_tmp_path = os.path.join(res, 'Logs/result_tmp.txt')
    logging.info("result_tmp_path: " + str(result_tmp_path))
    if os.path.exists(result_tmp_path):
        logging.info("resul_tmp_path存在，移动并重命名")
        new_result_tmp_path=os.path.join(res,'Logs/result_history/result_tmp_%s.txt'%(str(my_now)))
        shutil.move(result_tmp_path,new_result_tmp_path)

        #os.remove(result_tmp_path)
    else:
        logging.info("result_tmp_path不存在,忽略")
    #result_path=os.path.join(res,'Logs/result.txt')
    logging.info("result_path: "+str(result_path))
    if os.path.exists(result_path):
        logging.info("result_path 存在，移动名重命名")
        new_result_path = os.path.join(res, 'Logs/result_history/result_%s.txt' % (str(my_now)))
        shutil.move(result_path, new_result_path)
        return new_result_path
        #os.remove(result_path)
    else:
        logging.info("result_path不存在,忽略")
        return None


def save_result_tmp(upline,line):
    upline=str(upline)
    line=str(line)
    logging.info("将结果临时保存到txt中")
    logging.info("result_tmp_path: "+str(result_tmp_path))
    with open(result_tmp_path,'a',encoding='utf-8') as f:
        f.write(upline)
        f.write(line)
        f.write('\n')

def save_result_tmp_1(upline,line):
    # result_tmp_path_1 = os.path.join(res, 'Logs/result_tmp_1.txt')
    upline=str(upline)
    line=str(line)
    #logging.info("将第一次结果临时保存到txt中")
    #logging.info("result_tmp_path_1: "+str(result_tmp_path_1))
    with open(result_tmp_path_1,'a',encoding='utf-8') as f:
        f.write(upline)
        f.write(line)
        f.write('\n')
    #return result_tmp_path_1


def save_result():
    logging.info("处理结果")
    result=[]
    first_result=[]
    final_result=[]
    if os.path.exists(result_tmp_path):

        if os.path.exists(result_tmp_path_1):
            logging.info("第一次拉取的日志中存在唤醒日志...")
            with open(result_tmp_path_1,'r',encoding='utf-8') as f:
                lines=f.readlines()
                for line in lines:
                    first_result.append(line)
        else:
            logging.info("第一次拉取的日志中没有唤醒日志，不做处理,处理非第一次的日志即可。")

        with open(result_tmp_path,'r',encoding='utf-8') as f:
            lines=f.readlines()
            for line in lines:
                #result.append(line)
                logging.info("检查列表中是否有重复的")
                if line in result:
                    logging.info("列表中已存在该行，略过")
                else:
                    logging.info("列表中没有该行，保存........")
                    result.append(line)
        # print(result)
        # print(len(result))

        if first_result:
            logging.info("如果第一次拉取的日志中有唤醒日志，需要过滤")
            for line in result:
                if line in first_result:
                    logging.info(str(line)+"存在第一次日志中，过滤")
                else:
                    logging.info(str(line) + "不存在第一次日志中，保存")
                    final_result.append(line)
        else:
            logging.info("第一次拉取的日志中没有唤醒日志....")
            final_result=result


        logging.info("保存最终结果到: "+str(result_path))
        with open(result_path,'a',encoding='utf-8') as f:
            for i in final_result:
                #print(i)
                f.write(i)
        return result_path

    else:
        logging.info("result_tmp_path不存在: "+str(result_tmp_path))
        logging.info("这说明没有被唤醒")
        return None
    #pass

def log_check(text,filepath,first_flag):
    #i用来标识是不是第一次拉取的日志，如果是第一次的需要在最后过来掉
    '''
    需要返回的是：唤醒词是否识别到 True/False          is_wake
                唤醒词所在的行内容,没有唤醒返回''    wake_line
                识别是否成功   True/False           is_indenty
                识别成的字符串                       identy_str
                配置文件中读取的与语音词               real_str
    '''
    is_wake = False
    wake_line = ''
    is_indenty = False
    identy_str = ''
    real_str = ''
    nlp_str = ''
    if first_flag:
        logging.info("处理第一次拉取的日志")
        with open(filepath, encoding='utf-8') as f:
            lines = f.readlines()
            upline=''
            for line in lines:
                line = str(line)
                line = line.strip('\n')
                # 提取唤醒关键词
                pattern_wakeup = re.compile(r'.*?uaibot(.*?)\[app\]\[onWakeup\]\sapp\s\-\swakeup\:\sxiaoyouxiaoyou')
                matchObj_wakeup = re.match(pattern_wakeup, line)
                if matchObj_wakeup:
                    logging.info("正则匹配到了")
                    logging.info("matchObj_wakeup.group: " + str(matchObj_wakeup.group()))
                    logging.info("matchObj_wakeup.group(1): " + str(matchObj_wakeup.group(1)))
                    logging.info("输出该行： " + str(line))
                    is_wake = True
                    wake_line = line
                    text.insert(END,"正则匹配到了")
                    text.insert(END,str(line))
                    text.insert(END, '\n')
                    save_result_tmp_1(upline,line)
                upline=line

        return is_wake, wake_line
    # 返回的参数分别是：唤醒词是否识别到、唤醒词所在的行、交互是否识别成功、交互识别成的字符、配置文件中读取到的字符
    else:
        logging.info("处理非第一次的日志")
        with open(filepath, encoding='utf-8') as f:
            lines = f.readlines()
            upline = ''
            for line in lines:
                line = str(line)
                line = line.strip('\n')
                # 提取唤醒关键词
                pattern_wakeup = re.compile(r'.*?uaibot(.*?)\[app\]\[onWakeup\]\sapp\s\-\swakeup\:\sxiaoyouxiaoyou')
                matchObj_wakeup = re.match(pattern_wakeup, line)
                if matchObj_wakeup:
                    logging.info("正则匹配到了")
                    logging.info("matchObj_wakeup.group: " + str(matchObj_wakeup.group()))
                    logging.info("matchObj_wakeup.group(1): " + str(matchObj_wakeup.group(1)))
                    logging.info("输出该行： " + str(line))
                    is_wake = True
                    wake_line = line
                    text.insert(END, "正则匹配到了")
                    text.insert(END, str(line))
                    text.insert(END, '\n')
                    save_result_tmp(upline, line)
                upline = line
        return is_wake, wake_line


if __name__=='__main__':
    #clear_result()
    delete_files()

    #save_result()
    # now=time.time()
    # print(now)
    # timeArray=time.localtime(now)
    # print(timeArray)
    # my_now=time.strftime("%Y_%m_%d_%H_%M_%S",timeArray)
    # print(my_now)