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

def getTitle(url):
    Title = ''
    arr=[]
    str_1=url
    arr=str_1.split('/')
    Title=arr[-1]
    return Title


def getPicNum(htmlParser):
    picnum=0
    div = htmlParser.find('div', class_='img-list')
    imgList = div.findAll('img')
    picnum = len(imgList)
    return picnum

def getImgUrlList(htmlParser):
    imgUrlList=[]
    div = htmlParser.find('div', class_='img-list')
    imgList = div.findAll('img', class_='lazy')
    if imgList is not None:
        for imgitem in imgList:
            attrs=imgitem.attrs
            imgurl=str(attrs['data-original'])
            imgUrlList.append(imgurl)
    return imgUrlList

# def getUrlList(url, index):
#     print(index)
#     try:
#         html = requests.get(url)
#     except error.HTTPError as e:
#         return e
#     else:
#         html.encoding = 'utf-8'
#         bsObj = BeautifulSoup(html.text, 'html.parser')
#         div = bsObj.findAll('div', class_='link_btn')
#         if div is not None:
#             for tag_a in div:
#                 p=tag_a.find('a')
#                 urlList.append(p.get('href'))

#         pagenext = bsObj.find('div', class_='next')
#         now_page_index=int(bsObj.find('p', id='now_page').get_text())
#         pagemax=int(bsObj.find('p', id='last_page').get_text())
#         if pagenext is not None:
#             url_str=url
#             param_arr=url_str.split('/')
#             if now_page_index <= pagemax and now_page_index <= 10:
#                 now_page_index=now_page_index+1
#                 if param_arr[-3]=='page':
#                     param_arr[-2]=now_page_index
#                     url_next='/'.join(str(i) for i in param_arr)
#                     getUrlList(url_next, now_page_index)
#         return urlList
        
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
            string ='./'+parent_file+'/'+file+'/_'+str(num+1) + '.jpg'
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            num += 1
        if num >= numPicture:
            return

def doImage(url,title):
    url = url
    num_index = 0
    numPicture = 0
    parent_file='单页'
    # Title = getTitle(url)
    Title=title
    htmlparser = getHtmlParser(url)
    numPicture = getPicNum(htmlparser)
    imglist = getImgUrlList(htmlparser)  # 获取当前图片列表
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
    ids='297495'
    title='[竜胆、楠木りん] 粘獄のリーゼ 淫罪の宿命'
    doImage('https://hcomic1.com/cn/g2/'+ids+'/',title)
    print("全部任务完成")