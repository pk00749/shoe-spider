#encoding:utf-8

import configparser as ConfigParser
import os

class Login_info:

    def __init__(self):
        self.cf = ConfigParser.ConfigParser()
        # file_path = ".."+os.sep+"config"+os.sep+"config.ini" # 用os.sep来实现跨平台, config.ini文件要在同一个文件夹下
        file_path = os.path.dirname(os.path.realpath(__file__))+os.sep+'..'+os.sep+"login_info"+os.sep+"info.ini"
        # 用os.sep来实现跨平台, config.ini文件要在同一个文件夹下
        self.is_file_exist = True
        
        if os.path.exists(file_path):
            self.cf.read(file_path)
        else:
            self.is_file_exist = False
            print("info.ini file doesn't exist!")
    
    def get_info_version(self):
        # This method is for user to get the version of the config program
        
        if self.is_file_exist is False:
            print("Error: Cannot get the version value!")
            return
        
        str_version = self.cf.get("version", "version")  # 获取版本信息
        return str_version
    
    def get_info_info(self, account):
        """
        This method is for user to get the database info which is stored in the config.ini file
        """
        if self.is_file_exist is False:
            print("Error: Cannot get the database value!")
            return
        
        nike_items = self.cf.options(account)  # 判断信息是否足够
        if 'username' not in nike_items:
            print("please input username in the info.ini file")
            raise IOError
        elif 'password' not in nike_items:
            print("please input password in the info.ini file")
            raise IOError

        username = self.cf.get(account, "username")
        password = self.cf.get(account, "password")
        return {'username': username,
                'password': password
                }


if __name__ == '__main__':
    huya_config = Login_info()
    version = huya_config.get_info_version()  # get the version
    nike = huya_config.get_info_info("nike_1")
