# coding=utf-8
import datetime
import os
import random
import time

import ddddocr
from Mushishi.base.find_element import FindElement
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By


class RegisterFunction(object):
    def __init__(self, url, i):
        self.driver = self.get_driver(url, i)

    # 获取driver并且打开url,多浏览器运行
    def get_driver(self, url, i):
        if i == 1:
            driver = webdriver.Chrome()
        elif i == 2:
            driver = webdriver.Firefox()
        else:
            driver = webdriver.Edge()
        driver.get(url)
        driver.maximize_window()
        return driver

    # 输入用户信息
    def send_user_info(self, key, data):
        self.get_user_element(key).send_keys(data)

    # 定位用户信息，获取element
    def get_user_element(self, key):
        find_element = FindElement(self.driver)
        user_element = find_element.get_element(key)
        return user_element

    # 获取随机数
    def get_range_user(self):
        user_info = ''.join(random.sample('1234567890abcdefghijklmn', 8))
        return user_info

    def get_image_dir(self):
        screenshot_dir = r'E:\Python3913\Py39Projects\Mushishi\Image'  # 当前目录下的screenshot文件夹；或设置其他目录
        if not os.path.exists(screenshot_dir):  # 不存在则创建该目录
            os.mkdir(screenshot_dir)

        nowdate = datetime.datetime.now().strftime('%Y%m%d')  # 当日日期
        screenshot_today_dir = os.path.join(screenshot_dir, nowdate)  # 当前日期文件夹
        if not os.path.exists(screenshot_today_dir):
            os.mkdir(screenshot_today_dir)  # 不存在则创建

        nowtime = datetime.datetime.now().strftime('%H%M%S%f')  # 时间戳
        file = nowtime + ".png"  # 拼接文件名 时间戳+文件名+.png
        filepath = os.path.join(screenshot_today_dir, file)

        return filepath  # 截图，文件名=filename+时间戳

    # 获取验证码
    def get_code_image(self, file_name):
        code_element = self.driver.find_element(by=By.ID, value="getcode_num")  # 获取验证码元素
        left = code_element.location['x']
        top = code_element.location['y']
        right = code_element.size['width'] + left
        height = code_element.size['height'] + top
        self.driver.get_screenshot_as_file(file_name)
        im = Image.open(file_name)
        img = im.crop((left, top, right, height))
        img.save(file_name)
        print(img.save(file_name))

    # 解析图片获取验证码
    def code_online(self, file_name):
        self.get_code_image()
        ocr = ddddocr.DdddOcr()
        with open(file_name, 'rb') as f:
            img_bytes = f.read()
        text = ocr.classification(img_bytes)
        return text
        print(text)

    def main(self):
        user_name_info = self.get_range_user()
        user_email = user_name_info + "@163.com"
        '''
        image_info = self.get_image_dir()
        image = image_info.join(file)
        file_name = image
        code_text = self.code_online(file_name)
        '''
        self.send_user_info('user_email', user_email)
        self.send_user_info('user_name', user_name_info)
        self.send_user_info('password', "111111")
        self.send_user_info('code_text', code_text)
        self.get_user_element('register_button').click()
        code_error = self.get_user_element("code_text_error")
        if code_error is None:
            print("注册成功")
        else:
            self.driver.save_screenshot("E:\Python3913\Py39Projects\Mushishi\Image\codeerror.png")
        time.sleep(30)
        self.driver.close()


if __name__ == '__main__':
    for i in range(3):
        register_function = RegisterFunction('http://www.5itest.cn/register', i=1)
        register_function.main()
