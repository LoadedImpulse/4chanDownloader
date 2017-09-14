import urllib.request
import os
import time
import math
import datetime
import signal
import sys
import argparse
from bs4 import BeautifulSoup

def main():
    parser = argparse.ArgumentParser(description="Automatic refreshing 4chan image downloader")
    parser.add_argument('-w',type=str,required = True,help="URL of the website")
    parser.add_argument('-r', type=int,required = True,help="Refresh time of the website(seconds)")
    args = parser.parse_args()
    
    signal.signal(signal.SIGINT, handler)
    
    try:
        urllib.request.Request(args.w)
    except:
        print("Unknown URL adress entered, please try again")
        sys.exit(0)
    while True:
        downloadImages(args.w,args.r)

def handler(signum,frame):
    print("\n" + timeStamp() + "Exiting....")
    sys.exit(0)

def timeStamp():
    return ("[" + datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S') + "] \t " )

def createFolder(board,thread):
    currentPath = os.getcwd()
    directory = os.path.join(currentPath,'4chan-downloads',board,thread)
    if not os.path.exists(directory):
        os.makedirs(directory)
        print (timeStamp() + "Created a folder at: " + directory)
        
    return directory

def downloadImages(threadLink, timeToSleep):
    try:
        boardName = threadLink.split('/')[3]
        threadNum = threadLink.split('/')[5]
        workingDirectory = createFolder(boardName,threadNum)
        try:
            request = urllib.request.Request(threadLink,data = None,headers ={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
            site = urllib.request.urlopen(request)
        except urllib.error.HTTPError as error:
            print(error.args)
            sys.exit(0)

        soup = BeautifulSoup(site,'html.parser')
        exFiles = os.listdir(workingDirectory)
        if(len(exFiles) > 0):
            print(timeStamp() + "Found " + str(len(exFiles)) + " previous file(s)")
        else:
            print(timeStamp() + "No previous files detected")
        
        totalDownloads = 0
        for link in soup.find_all("a", {"class" : "fileThumb"}):
            fileName = link.get('href').split('/')[4]
            if(fileName not in exFiles):
                print(timeStamp() + "Downloading: " + fileName, end="")
                urllib.request.urlretrieve("http:" + link.get('href'),(workingDirectory +"/" + fileName)) 
                print(" \t[DONE]");
                totalDownloads += 1
        print(timeStamp() + "Downloaded " + str(totalDownloads) + " file(s), skipped " + str(len(exFiles)) + " file(s)")
        print(timeStamp() + "Refreshing after " + str(timeToSleep) + " seconds")
        for i in range(timeToSleep):
            if(timeToSleep > 10 and i == math.floor((timeToSleep / 2))):
                print(timeStamp() + "Refreshing in " + str(math.ceil((timeToSleep / 2))) + " seconds")
            time.sleep(1)
        print(timeStamp() + "Refreshing... \n")
        time.sleep(1)
        
    except IndexError:
        print(timeStamp() + "Error occured, please restart")
        sys.exit(0)
        
if __name__ == "__main__":
	main()