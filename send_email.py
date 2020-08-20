import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email import encoders
from email.mime.base import MIMEBase
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import datetime
from openpyxl import load_workbook
import os

import logging
import logging.config

CON_LOG='log.conf'
logging.config.fileConfig(CON_LOG)
logging=logging.getLogger()

def my_send_email(msg_to,file_path,test_time):
    logging.info("开始发送邮件")
    if file_path==None:
        file_path='none.txt'

    now_time = datetime.datetime.now()
    year = now_time.year
    month = now_time.month
    day = now_time.day
    mytime = str(year) + " 年 " + str(month) + " 月 " + str(day) + " 日 "
    msg_from = '1508691067@qq.com'  # 发送方邮箱
    passwd = 'fgaplzfksqsihdbe'

    subject = '语音误唤醒测试结果'

    #首先要判断file_path里面有没有内容，有内容表明有误唤醒的情况
    #并且要提取出个数


    if os.path.exists(file_path) and os.path.getsize(file_path)!=0:
        logging.info("存在误唤醒，发送格式1")
        with open(file_path,'rb') as f:
            lines=f.readlines()
            wake_nums=len(lines)
    #构造要发送的内容格式
        content = '''
                    <html>
                    <body>
                        <h1 align="center">智能音响语音误唤醒测试结果</h1>
                        <p><strong>您好：</strong></p>
                        <blockquote><p><strong>测试时长(h): {test_time}</strong></p></blockquote>
                        <blockquote><p><strong>误唤醒次数: {wake_nums}</strong></p></blockquote>
                        <blockquote><p><strong>附件是语音误唤醒测试结果,请查收！</strong></p></blockquote>
    
    
                        <p align="right">{mytime}</p>
                    <body>
                    <html>
                    '''.format(test_time=test_time,wake_nums=wake_nums,mytime=mytime)
    else:
        logging.info("不存在误唤醒，发送格式2")
        # 构造要发送的内容格式
        content = '''
                            <html>
                            <body>
                                <h1 align="center">智能音响语音误唤醒测试结果</h1>
                                <p><strong>您好：</strong></p>
                                <blockquote><p><strong>测试时长(h): {test_time}</strong></p></blockquote>
                                <blockquote><p><strong>误唤醒次数: 0</strong></p></blockquote>
                                
                                <p align="right">{mytime}</p>
                            <body>
                            <html>
                            '''.format(test_time=test_time, mytime=mytime)
    # 这个应该就是构建了要给html对象
    msg = MIMEMultipart()
    msg.attach(MIMEText(content, 'html', 'utf-8'))

    if os.path.exists(file_path) and os.path.getsize(file_path) != 0:
        logging.info("存在误唤醒，发送附件")
        #构造附件
        att1=MIMEText(open(file_path,'rb').read(),'base64','utf-8')
        att1['Content-Type']='application/octet-stream'
        file_base_path=os.path.dirname(file_path)  #获取路径
        file_base_name=os.path.basename(file_path)  #获取文件名称
        att1['Content-Disposition'] = 'attachment;filename=' + file_base_name
        msg.attach(att1)


    #logging.info("没有误唤醒，不发送附件")
    # 放入邮件主题
    msg['Subject'] = subject

    # 放入发件人,这是展示在邮件里面的，和时间的发件人没有关系
    msg['From'] = msg_from
    try:
        # 通过ssl方式发送，服务器地址，端口
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        # 登录邮箱
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        # print("邮件发送成功")
        logging.info("邮件发送成功")
    except Exception as e:
        # print(e)
        logging.error("发送邮件失败")
        logging.error(e)
    finally:
        logging.info("结束发送邮件")
        s.quit()


if __name__=="__main__":
    filepath='D:\\Python_Project\\False_wake\Logs\\result_history\\result_2020_07_21_14_33_55.txt'

    msg_to = ['1508691067@qq.com']
    my_send_email(msg_to,filepath,5)