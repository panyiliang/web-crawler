# -*- coding: utf-8 -* 
import re
import requests
from urllib import error
from bs4 import BeautifulSoup
import os
import asyncio
from aiohttp import ClientSession
import time

file = ''
List = []
urlList = []

def getHtml(url):
    try:
        html = requests.get(url)
    except error.HTTPError as e:
        return e
    else:
        html.encoding = 'utf-8'
        htmlbody = BeautifulSoup(html.text, 'html.parser')
    return htmlbody

def getTitle(htmlbody):
    print("获取标题：")
    print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    Title = ''
    div = htmlbody.find('h1', class_='single')
    Title = div.get_text()
    return Title    

def getImageUrl(htmlbody):
    print("获取图片地址：")
    print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    imageurl=''
    div = htmlbody.find('h1', class_='single-img')
    img = div.find('img')
    imageurl = img.get('src')
    return imageurl

def getPicNum(htmlbody):
    print("获取图片数量：")
    print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    pic_num=0
    p = htmlbody.find('p', id='max_img')
    pic_num = int(p.get_text())
    return pic_num

def reduceUrlList(url, picnum):
    print("重组图片下载地址：")
    print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    piclist=[]
    str_1=''
    arr_1=[]
    str_1 = url
    arr_1 = str_1.split('/')
    arr_next=arr_1
    img_name=arr_1[-1]
    img_arr=img_name.split('-')
    img_index=int(img_arr[1])
    piclist.append(url)
    while img_index<picnum:
        img_index+=1
        img_next_index=img_index
        if(img_index>=10):
            img_arr[1]='0'+str(img_next_index)
        else:
            img_arr[1]='00'+str(img_next_index)
        img_next_name='-'.join(str(i) for i in img_arr)
        arr_next[-1]=img_next_name
        url_next='/'.join(str(i) for i in arr_next)
        piclist.append(url_next)
    return piclist

def dowmloadPicture(pic_url, numPicture, parent_file, file, num):
    for each in pic_url:
        print('正在下载第' + str(num + 1) + '张图片')
        print('下载地址：'+ each)
        try:
            if each is not None:
                pic = requests.get(each, timeout=100)
            else:
                continue
        except BaseException:
            print('错误，当前图片无法下载:' + each)
            num += 1
            continue
        else:
            string ='./'+parent_file+'/'+file+'/_'+str(num+1) + '.jpg'
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            num += 1
        if num >= numPicture:
            return

def doImage():
    url=''
    Title='レムの妄想エッチオナニー本'
    firsturl='http://img-doujin-free5.com/thumb640_2/img858b2597e96bb7/58b2597e96bb7-001-640.jpg'
    num_index = 0
    parent_file = 'Re0'
    numPicture = 20
    urllist=reduceUrlList(firsturl, numPicture)
    print('图片数量：'+str(numPicture))
    file = Title
    y = Title
    if y == 1:
        os.mkdir(file +'_1')
    else:
        os.mkdir('./Re0/'+file)
    t = 0
    while t < numPicture:
        dowmloadPicture(urllist, numPicture, parent_file, file, num_index)
        num_index = num_index+1
        t = t + 60
    message = Title + " 下载完成"
    return message
 
if __name__ == '__main__':  # 主函数入口
    doImage()
    print("全部任务完成")