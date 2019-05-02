import threading, queue, time, os, pickle
from selenium import webdriver
import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ActionChains
from module.login_info import Login_info
from module.config import Config
from PIL import Image

PHANTOMJS_MAX = 1

# logging.basicConfig(level=logging.INFO,
#                     filename='../log/in_room.log',
#                     datefmt='%Y/%m/%d %H:%M:%S',
#                     format='%%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')

class conphantomjs:
    jiange = 0.00001  # 开启phantomjs间隔
    timeout = 20  # 设置phantomjs超时时间
    # path = "D:\python27\Scripts\phantomjs.exe"  ##phantomjs路径
    # service_args = ['--load-images=no', '--disk-cache=yes']  ##参数设置

    def __init__(self, account):
        self.logger = logging.getLogger(__name__)
        self.logger.info('Thread initialing...')

        self.config = Config()
        self.info = self.config.get_config_info()
        self.home_url = self.info["url"]
        self.phantomjs_max = PHANTOMJS_MAX  # 同时开启phantomjs个数
        self.q_phantomjs = queue.Queue()  # 存放phantomjs进程队列

        user_profile = Login_info()
        self.user_info = user_profile.get_info_info(account)
        self.username = self.user_info['username']
        self.password = self.user_info['password']

    def get_snap(self, driver, name):
        '''
        对整个网页截图，保存成图片，然后用PIL.Image拿到图片对象
        :return: 图片对象
        '''
        driver.save_screenshot('{pic}.png'.format(pic=name))
        page_snap_obj = Image.open('{pic}.png'.format(pic=name))
        return page_snap_obj

    def get_image(self, driver, name):
        '''`
        从网页的网站截图中，截取验证码图片
        :return: 验证码图片
        '''
        wait = WebDriverWait(driver, 10)
        img = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        time.sleep(2)  # 保证图片刷新出来
        location = img.location
        size = img.size

        top = location['y']
        bottom = location['y'] + size['height']
        left = location['x']
        right = location['x'] + size['width']

        page_snap_obj = self.get_snap(driver, name)
        crop_imag_obj = page_snap_obj.crop((left, top, right, bottom))
        return crop_imag_obj

    def get_distance(self, image1, image2):
        '''
        拿到滑动验证码需要移动的距离
        :param image1:没有缺口的图片对象
        :param image2:带缺口的图片对象
        :return:需要移动的距离
        '''
        threshold = 60
        left = 57
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                rgb1 = image1.load()[i, j]
                rgb2 = image2.load()[i, j]
                res1 = abs(rgb1[0] - rgb2[0])
                res2 = abs(rgb1[1] - rgb2[1])
                res3 = abs(rgb1[2] - rgb2[2])
                if not (res1 < threshold and res2 < threshold and res3 < threshold):
                    return i - 10  # 经过测试，误差为大概为7
        return i - 10  # 经过测试，误差为大概为7

    def get_tracks(self, distance):
        '''
        拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
        匀变速运动基本公式：
        ①v=v0+at
        ②s=v0t+½at²
        ③v²-v0²=2as

        :param distance: 需要移动的距离
        :return: 存放每0.3秒移动的距离
        '''
        # 初速度
        v = 0
        # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
        t = 0.3
        # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
        tracks = []
        # 当前的位移
        current = 0
        # 到达mid值开始减速
        mid = distance * 4 / 5

        while current < distance:
            if current < mid:
                # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
                a = 2
            else:
                a = -3

            # 初速度
            v0 = v
            # 0.2秒时间内的位移
            s = v0 * t + 0.5 * a * (t ** 2)
            # 当前的位置
            current += s
            # 添加到轨迹列表
            tracks.append(round(s))

            # 速度已经达到v,该速度作为下次的初速度
            v = v0 + a * t
        return tracks

    def getbody(self):
        """利用phantomjs获取网站源码以及url"""
        d = self.q_phantomjs.get()
        print('driver id: ' + str(d))
        print('opening url: %s' % self.home_url)
        # d.maximize_window()
        d.get(self.home_url)
        print('logging, user name: %s' % self.username)
        wait = WebDriverWait(d, 20)
        #//*[@id="loginName"] //*[@id="loginName"]
        input_name = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='loginName']")))
        # ele = d.find_element_by_xpath('//*[@id="loginName"]') #loginName
        # ele.send_keys(self.username)
        # input_name.clear()
        input_name.send_keys(self.username)
        #//*[@id="loginPass"]
        input_password = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='loginPass']")))
        input_password.send_keys(self.password)
        time.sleep(2)
        button = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'geetest_radar_tip')))
        button.click()
        time.sleep(1)
        # 步骤二：拿到没有缺口的图片
        d.execute_script('document.querySelectorAll("canvas")[2].style=""')
        image1 = self.get_image(d, 'ori')
        # 步骤三：点击拖动按钮，弹出有缺口的图片
        button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_slider_button')))
        button.click()
        # 步骤四：拿到有缺口的图片
        image2 = self.get_image(d, 'after')

        print(image1,image1.size)
        print(image2,image2.size)
        # 步骤五：对比两张图片的所有RBG像素点，得到不一样像素点的x值，即要移动的距离
        distance = self.get_distance(image1, image2)

        # 步骤六：模拟人的行为习惯（先匀加速拖动后匀减速拖动），把需要拖动的总距离分成一段一段小的轨迹
        tracks = self.get_tracks(distance)
        print('tracks:')
        print(tracks)
        print(image1.size)
        print(distance, sum(tracks))

        # 步骤七：按照轨迹拖动，完全验证
        button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_slider_button')))
        ActionChains(d).click_and_hold(button).perform()
        for track in tracks:
            ActionChains(d).move_by_offset(xoffset=track, yoffset=0).perform()
        else:
            ActionChains(d).move_by_offset(xoffset=3, yoffset=0).perform()  # 先移过一点
            ActionChains(d).move_by_offset(xoffset=-3, yoffset=0).perform()  # 再退回来，是不是更像人了

        time.sleep(0.5)  # 0.5秒后释放鼠标
        ActionChains(d).release().perform()
        time.sleep(20)
        # 步骤八：完成登录
        login = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="guestLogin"]/div[2]/div[5]')))
        #//*[@id="guestLogin"]/div[2]/div[5]
        login.click()
        time.sleep(20)

        self.q_phantomjs.put(d)

    def open_phantomjs(self):
    #     """多线程开启phantomjs进程"""
        def open_threading():
            chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
            os.environ["webdriver.chrome.driver"] = chromedriver
            desired_capabilities = DesiredCapabilities.CHROME
            desired_capabilities["pageLoadStrategy"] = "none"
            option = webdriver.ChromeOptions()
            d = webdriver.Chrome(chromedriver, chrome_options=option)

            self.q_phantomjs.put(d)  # 将phantomjs进程存入队列

        th = []
        for i in range(self.phantomjs_max):
            t = threading.Thread(target=open_threading)
            th.append(t)
        for i in th:
            i.start()
            time.sleep(conphantomjs.jiange)  # 设置开启的时间间隔
        for i in th:
            i.join()

    def close_phantomjs(self):
        """多线程关闭phantomjs对象"""
        th = []

        def close_threading():
            d = self.q_phantomjs.get()
            d.quit()

        for i in range(self.q_phantomjs.qsize()):
            t = threading.Thread(target=close_threading)
            th.append(t)
        for i in th:
            i.start()
        for i in th:
            i.join()

    def main(self):
        # 1. check cookies exist or not. if not, give cookies

        # 2. run open_phantomjs, create the process of phantomjs
        # self.phantomjs_max = 1
        self.open_phantomjs()
        print("phantomjs num is ", self.q_phantomjs.qsize())

        th = []
        t = threading.Thread(target=cur.getbody)
        th.append(t)
        for i in th:
            i.start()
        for i in th:
            i.join()

        self.close_phantomjs()
        print("phantomjs num is ", self.q_phantomjs.qsize())



if __name__ == "__main__":
    cur = conphantomjs('nike_1')
    cur.main()