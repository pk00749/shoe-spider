# -*- coding: utf-8 -*-
import random
import time, re, os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import requests
from io import BytesIO

EMAIL = 'test@test.com'
PASSWORD = '123456'


class CrackGeetest():
    def __init__(self):
        self.url = 'https://account.geetest.com/login'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.pasword = PASSWORD

    def get_geetest_button(self):
        button = self.wait.until(EC.element_to_be_clickable((BY.CLASS_NAME, 'geetest_radar_tip')))
        return button

    # 点击验证按钮
    button = self.get_geetest_button()
    button.click()

    #
    # 获取位置和size
    def position(self):
        img = self.wait.until(EC.persence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return (top, bottom, left, right)

    # 获取网页截图
    def get_geetest_image(self, name='captcha.png'):
        top, bottom, left, right = self.get_position()  # 获取图片的位置和宽高，随后返回左上角和右下角的坐标
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()  # 得到屏幕目标
        captcha = screenshot.crop((left, top, right, bottom))

    # 获取第二张图片（带有缺口的图片）
    def get_slider(self):
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    # 点击后出现接口
    slider = self.get_slider()
    slider.click()
    # 在调用 get_geetest_image()函数获取第二张图，分别命名为img1和img2
    '''
    对比图像的缺口，需要遍历图片的每一个坐标点，获取两张图片对应像素点的RGB数据，如果差距在一定范围内，则代表两个像素相同，接着继续对比下一个像素点。如果差距在一定范围之外，则说明不是相同的像素点，则该位置就是缺口位置
    '''

    def is_pixel_equal(self, img1, img2, x, y):
        # 取两个图片的像素点
        pixel1 = img1.load()[x, y]
        pixel2 = img2.load()[x, y]
        threshold = 60
        # 两张图RGB的绝对值小于定义的阈值，则代表像素点相同，继续遍历。否则不相同，为缺口位置
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_gap(self, img1, img2):
        left = 60
        for i in range(left, img1.size[0]):
            for j in range(img1.size[1]):
                if not self.is_pixel_equal(img1.img2, i, j):  # 判断两个图片的某一点的像素是否相同
                    left = i
                    return left
        return left

    def get_track():
        track = []
        current = 0
        mid = distance * 4 / 5
        t = 0.2
        v = 0
        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3
            v0 = v
            v = v0 + a * t
            x = v0 * t + 1 / 2 * a * t ^ 2
            move = v0 * t + 1 / 2 * a * t ^ 2
            current += move
            track.append(round(move))
        return track

    def move_to_gap(self, slider, tracks):
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in tracks:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.3)
        ActionChains(self.browser).release().perform()