#!/usr/bin/env python
# encoding: utf-8

import os
import json
import requests

#获取无水印视频地址


def getResultUrl(url):

    #设置请求头的UA信息，将之设置为移动设备
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.0.3; zh-cn; U8860 Build/HuaweiU8860) UC AppleWebKit/530+ (KHTML, like Gecko) Mobile Safari/530'}
    res = requests.get(url, headers=headers)

    #获取接口id
    re_url = res.url
    item_id = re_url.split("/video/")[1].split("/")[0]

    #获取dytk
    re_text = res.text
    dytk = re_text.split('dytk: "')[1].split('"')[0]

    #设置iteminfo请求url
    item_url = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=" + \
        item_id + "&dytk =" + dytk
    item_res = requests.get(item_url, headers=headers)

    #获取到 item_ids 和 dytk后，可通过 iteminfo接口获取到无水印链接。

    #获取无水印链接
    data = json.loads(item_res.text)
    result_url = data['item_list'][0]['video']['play_addr']['url_list'][1]

    return result_url

    #测试代码
    # print(dytk)
    # print(item_id)
    # print(item_res.json())
    # print(data['item_list'][0]['video']['play_addr']['url_list'][1])


# 测试数据
# url = "https://v.douyin.com/bmnGh6"
# print(getResultUrl(url))

def download(url):

    root = os.path.dirname(os.path.realpath(__file__))
    path = root+"\\"+url.split('com/')[1].split('/')[0]+".mp4"

    result_url = getResultUrl(url)

    try:
        if not os.path.exists(root):  # 这个文件夹不存在，
            os.mkdir(root)  # 创建这一个文件
        if not os.path.exists(path):  # 这一个文件不存在
            r = requests.get(result_url)
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
                print("保存成功")
        else:
            print("文件已存在")
    except:
        print("爬取失败")


url = input("url：")
download(url)
