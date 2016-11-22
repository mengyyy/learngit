# !/usr/bin/env  python
# -*- coding: utf-8 -*-

from multiprocessing import Process, Manager
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import os
import re
import time

myyhread = 15
manager = Manager()
FileList = []
FileList = manager.list()
DireList = []
DirList = manager.list()
file_type = '^[^?/].*[^/]$'
dir_type = "^[^/.].*\/$"
downloadDirectory = 'mengyyy_'
baseUrl = 'http://ru.mengyyy.xyz/'


def getAbsolutedURL(baseUrl, source):
    if source.startswith('http://www.'):
        url = 'http://' + source[11:]
    elif source.startswith('http://'):
        url = source
    elif source.startswith('www.'):
        url = source[4:]
        url = 'http://' + source
    else:
        url = baseUrl + '/' + source
    if baseUrl not in url:
        return None
    return url


def getDownloadPath(baseUrl, absoluteUrl, downloadDirectory):
    path = absoluteUrl.replace('http://', '')
    path = path.replace('www.', '')
    path = path.replace(baseUrl, '')
    path = re.sub('js\?.*', 'js', path)
    path = downloadDirectory + path
    print('path is ' + path)
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return path


def getFile(name, baseUrlList):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    for fileUrl in baseUrlList:
        urlretrieve(fileUrl, getDownloadPath(
                    baseUrl, fileUrl, downloadDirectory))
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))


def get_file_link(baseUrl):
    html = urlopen(baseUrl)
    bsObj = BeautifulSoup(html, 'html.parser')
    dir_link_list = bsObj.findAll('a', href=re.compile(dir_type))
    file_link_list = bsObj.findAll('a', href=re.compile(file_type))
    for fl in file_link_list:
        FileList.append(baseUrl + fl.attrs['href'])
        print('get file link | {}'.format(baseUrl + fl.attrs['href']))
    if len(dir_link_list) > 0:
        for dl in dir_link_list:
            print('enter dir | {}'.format(baseUrl + dl.attrs['href']))
            get_file_link(baseUrl + dl.attrs['href'])

if __name__ == '__main__':
    threads_getlink = []
    print('------------------------start------------------------')
    ts = time.time()
    get_file_link(baseUrl)
    for ff in FileList:
        print(ff)
    print('time use {:.4f}'.format(time.time() - ts))
    print('------------------------end------------------------')
    print(len(FileList))
    ts = time.time()
    threads_download = []
    for ll in range(myyhread):
        t = Process(target=getFile, args=(ll, FileList[ll::myyhread]))
        t.daemon = True
        threads_download.append(t)

    for i in range(len(threads_download)):
        threads_download[i].start()

    for j in range(len(threads_download)):
        threads_download[j].join()
    print('time use {:.4f}'.format(time.time() - ts))
    print('------------------------end------------------------')
    exit()


