# -*- coding: utf-8 -* 
import re
import requests
from urllib import error
from bs4 import BeautifulSoup
import os
import asyncio
from aiohttp import ClientSession
import time

num_1 = 0
file = ''
List = []
urlList = []

def getHtmlParser(url):
    htmlParser=''
    try:
        html = requests.get(url)
    except error.HTTPError as e:
        return e
    else:
        html.encoding = 'utf-8'
        htmlParser = BeautifulSoup(html.text, 'html.parser')
    return htmlParser

def getTitle(htmlParser):
    Title = ''
    div = htmlParser.find('h1', class_='single')
    Title = div.get_text().replace("/","")
    return Title

def getFirstUrl(htmlParser):
    firsturl=''
    div = htmlParser.find('div', class_='single-img')
    p = div.find('img')
    firsturl = p.get('src')
    return firsturl

def getPicNum(htmlParser):
    picnum=0
    div = htmlParser.find('p', id='max_img')
    picnum = int(div.get_text())
    return picnum

def reduceUrlList(url, picnum):
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

def getUrlList(url, index):
    print(index)
    try:
        html = requests.get(url)
    except error.HTTPError as e:
        return e
    else:
        html.encoding = 'utf-8'
        bsObj = BeautifulSoup(html.text, 'html.parser')
        div = bsObj.findAll('div', class_='link_btn')
        if div is not None:
            for tag_a in div:
                p=tag_a.find('a')
                urlList.append(p.get('href'))

        pagenext = bsObj.find('div', class_='next')
        now_page_index=int(bsObj.find('p', id='now_page').get_text())
        pagemax=int(bsObj.find('p', id='last_page').get_text())
        if pagenext is not None:
            url_str=url
            param_arr=url_str.split('/')
            if now_page_index <= pagemax:
                now_page_index=now_page_index+1
                if param_arr[-3]=='page':
                    param_arr[-2]=now_page_index
                    url_next='/'.join(str(i) for i in param_arr)
                    getUrlList(url_next, now_page_index)
        return urlList
        
def dowmloadPicture(html, pic_url, numPicture, parent_file, file, num):
    for each in pic_url:
        print('正在下载第' + str(num + 1) + '张图片')
        # print('下载地址：'+ each)
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
            string ='./'+parent_file+'/'+file+'/'+str(num_1)+'_'+str(num+1) + '.jpg'
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            num += 1
        if num >= numPicture:
            return

def doImage(url):
    url = url
    parent_file = '媚薬'
    num_index = 0
    numPicture = 0
    htmlparser = getHtmlParser(url)
    Title = getTitle(htmlparser)
    firsturl = getFirstUrl(htmlparser)
    numPicture = getPicNum(htmlparser)
    imglist = reduceUrlList(firsturl, numPicture)  # 获取当前图片列表
    print('开始下载'+parent_file+'-'+Title)
    print('图片数量：'+str(numPicture))
    file = Title
    y = Title
    if y == 1:
        os.mkdir(parent_file+'/'+file +'_1')
    else:
        os.mkdir(parent_file+'/'+file)
    t = 0
    while t < numPicture:
        try:
            result = requests.get(url, timeout=1000)
            print(url)
        except error.HTTPError as e:
            print(e + '网络错误，请调整网络后重试')
            t = t+60
        else:
            dowmloadPicture(result.text, imglist, numPicture, parent_file, file, num_index)
            num_index = num_index+1
            t = t + 60
    message = Title + " 下载完成"
    return message
 
if __name__ == '__main__':  # 主函数入口
    picurl_list = getUrlList('http://doujin-free.com/tag/%e5%aa%9a%e8%96%ac/page/5/', 1) # 目标页面地址 
    for i in picurl_list:
        print("获取文章链接：")
        print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        picurl = i
        num_1 = num_1+1
        msg = doImage(picurl)
        print(msg)
    print("全部任务完成")