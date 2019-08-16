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

def getTitle(url):
    print("获取标题：")
    print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    Title = ''
    try:
        html = requests.get(url)
    except error.HTTPError as e:
        return e
    else:
        html.encoding = 'utf-8'
        bsObj = BeautifulSoup(html.text, 'html.parser')
        div = bsObj.find('h2', id='post_title')
        Title = div.get_text()
    return Title    
    
def recommend(url, pageindex, Re):
    print("获取图片列表：")
    print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    try:
        html = requests.get(url)
    except error.HTTPError as e:
        return e
    else:
        html.encoding = 'utf-8'
        bsObj = BeautifulSoup(html.text, 'html.parser')
        div = bsObj.find('div', class_='post_content')
        if div is not None:
            listA = div.findAll('img')
            for i in listA:
                if i is not None:
                    Re.append(i.get('src'))

        pagenext = bsObj.find('div', class_='post_pagination')
        if pagenext is not None:
          listB = pagenext.findAll('a')
          for i in listB:
            if i is not None:
              next_url = i.get('href')
              index = i.get_text()
              if int(index) > int(pageindex):
                recommend(next_url, index, Re)
        return Re

def getUrlList(url, index):
    print("获取文章列表：")
    print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    try:
        html = requests.get(url)
    except error.HTTPError as e:
        return e
    else:
        html.encoding = 'utf-8'
        bsObj = BeautifulSoup(html.text, 'html.parser')
        div = bsObj.find('div', id='post_list3')
        p = div.findAll('p', class_='post_thumbnail')
        if p is not None:
            for j in p:
                listA = j.findAll('a')
                for i in listA:
                    if i is not None:
                        urlList.append(i.get('href'))
                        
        # pagenext = bsObj.find('div', class_='page_navi')
        # if pagenext is not None:
        #     listC = pagenext.findAll('a')
        #     for i in listC:
        #         page_index = i.get_text()
        #         if page_index.isdigit():
        #             if i is not None and int(page_index)==index+1 and int(page_index)<=5:
        #                 next_url = i.get('href')
        #                 getUrlList(next_url, int(page_index))
        return urlList
        
def dowmloadPicture(html, pic_url, numPicture, file, num):
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
            string ='./'+file+'/'+str(num_1)+'_'+str(num+1) + '.jpg'
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            num += 1
        if num >= numPicture:
            return

def doImage(url):
    url = url
    Recommend = recommend(url, 1, [])  # 记录相关推荐
    Title = getTitle(url)
    print(Title)
    num_index = 0
    numPicture = 0
    numPicture = len(Recommend)
    print('图片数量：'+str(numPicture))
    file = Title
    y = Title
    if y == 1:
        os.mkdir(file +'_1')
    else:
        os.mkdir(file)
    t = 0
    while t < numPicture:
        try:
            result = requests.get(url, timeout=1000)
            print(url)
        except error.HTTPError as e:
            print(e + '网络错误，请调整网络后重试')
            t = t+60
        else:
            dowmloadPicture(result.text, Recommend, numPicture, file, num_index)
            num_index = num_index+1
            t = t + 60
    message = Title + " 下载完成"
    return message
 
if __name__ == '__main__':  # 主函数入口
    picurl_list = getUrlList('https://lovecomicz.com/?s=%E3%82%A8%E3%83%AD%E3%83%9E%E3%83%B3%E3%82%AC%E5%85%88%E7%94%9F', 1)  # 目标页面地址 
    for i in picurl_list:
        print("获取文章链接：")
        print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        picurl = i
        num_1 = num_1+1
        msg = doImage(picurl)
        print(msg)
    print("全部任务完成")