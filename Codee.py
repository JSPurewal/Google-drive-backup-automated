"""
@author: Jaskaran S. Purewal
"""

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from zipfile import ZipFile
import datetime as DT
import os
import schedule

path=r"C:\Users\Jaskaran S. Purewal\Documents\5th Sem\Cloud Computing\Backup Project\Backup"
path1=r"C:\Users\Jaskaran S. Purewal\Documents\5th Sem\Cloud Computing\Backup Project"
todayy=DT.date.today()
todayy=todayy.strftime("%d%m%Y")
today=todayy+".zip"
#Authentication and upload file to drive
def upp(ffile): 
    try:
        googleAuthen=GoogleAuth()

        googleAuthen.LoadCredentialsFile("mycreds.txt")
        if googleAuthen.credentials is None:
            googleAuthen.LocalWebserverAuth()
        elif googleAuthen.access_token_expired:
            googleAuthen.Refresh()
        else:
            googleAuthen.Authorize()
        
        googleAuthen.SaveCredentialsFile("mycreds.txt")
        
    except:
        return False
    gdrive=GoogleDrive(googleAuthen)


    f=gdrive.CreateFile({'title':today})
    f.SetContentFile(ffile)
    f.Upload()
        
    f=None
    print("Upload Successful.")
    return True
        
def allPaths():
    file_paths=[]
    for folder,subf,fil in os.walk(path):
     for filename in fil:
      filePath=os.path.join(folder,filename)
      file_paths.append(filePath)
    return file_paths





def zippin():
    file_paths=allPaths()
    count=0
        
    with ZipFile(today,'w') as zip:
        for file in file_paths:
            zip.write(file)
            count=count+1
    print("All Files zipped successfully:")
    print(count)

def getPath(filename,search_path):#today,path1
    for root,dir,files in os.walk(search_path):
        if filename in files:
            result=os.path.join(root,filename)
            break
    return result

def weekBeforeCheck():
    
    
    week_before=DT.date.today()-DT.timedelta(days=7)
    week_before=week_before.strftime("%d%m%Y")
    
    
    googleAuthen=GoogleAuth()

    googleAuthen.LoadCredentialsFile("mycreds.txt")
    if googleAuthen.credentials is None:
        googleAuthen.LocalWebserverAuth()
    elif googleAuthen.access_token_expired:
        googleAuthen.Refresh()
    else:
        googleAuthen.Authorize()
        
    googleAuthen.SaveCredentialsFile("mycreds.txt")
    
    gdrive=GoogleDrive(googleAuthen)
    
    query=f"title contains '{week_before}'"
    file_list=gdrive.ListFile({'q':query}).GetList()
    
    
    if not file_list:
        return False
    else:
        file_id=file_list[0]['id']
        file_del=gdrive.CreateFile({'id':file_id})
        file_del.Trash()
        return True
    
    
        
def logUpdate(check):
    log=open("log.txt","a")
    if(check==False):
        value=str(DT.datetime.now())+"  backup_failed    Could not connect to Drive.\n"
    else:
        value=str(DT.datetime.now())+"   backup_successfull   "+path+"\n"
        
    log.write(value)
    log.close()

def main():
    zippin()
    zzip=getPath(today,path1)
    check=upp(zzip)
    if(check==False):
        print("Error while connecting to drive.")
        
    removepath=os.path.join(path1,today)
    os.remove(removepath)
    if(check==True):
        #Week before check
        if(weekBeforeCheck()):
            print("Back up of 7 days before is deleted.")
        
        print("Today's Backup Successfull.")
            
    logUpdate(check)
    
    
    



if __name__=="__main__":
    main()
    schedule.every(1).minutes.do(main)
    #schedule.every().day.at("15:00").do(main)
    while(True):
        schedule.run_pending()