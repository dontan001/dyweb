
from selenium import webdriver
from time import sleep
import unittest

class LoginCase(unittest.TestCase):
    def setUp(self):
        self.dr = webdriver.Chrome(executable_path='/Users/dongtan/downloads/chromedriver')
        # chrome driver or phantom js
        self.dr.maximize_window()

    # 定义登录方法
    def login(self, username, password):
        self.dr.get('https://accounts.douban.com/login')
        self.dr.find_element_by_id('email').send_keys(username)
        sleep(3)
        self.dr.find_element_by_id('password').send_keys(password)
        sleep(3)
        self.dr.find_element_by_name('login').click()

    def test_login_success(self):
        self.login('1009137312@qq.com', 'FanTan879425')  # 正确用户名和密码
        sleep(3)
        link = self.dr.find_element_by_id('lnk_current_user')
        self.assertTrue('1009137312' in link.text)

    @unittest.skip('')
    def test_login_pwd_error(self):
        self.login('1009137312@qq.com', 'FanTan879426')  # 正确用户名，错误密码
        sleep(2)
        error_message = self.dr.find_element_by_id('tip_btn').text
        self.assertIn('pwd error', error_message)

    def tearDown(self):
        sleep(2)
        self.dr.quit()

if __name__ == '__main__':
    unittest.TextTestRunner().run()
