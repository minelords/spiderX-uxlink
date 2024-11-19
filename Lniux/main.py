from spider_x_uxlink import *
import threading
import math
import random
import configparser

class MyThread(threading.Thread):
    def __init__(self, passwd, invitecode, domain, yesclientkey, question, proxies, uxlinkinfo, proxy_flag, driver_flag, less):
        super().__init__()
        # X registration information
        self.url = "https://x.com/i/flow/signup"
        self.passwd = passwd
        # uxlink invite code
        self.invitecode = invitecode  # iter
        self.uxlinkinfo = uxlinkinfo  # iter
        self.domain = domain
        self.yesclientkey = yesclientkey
        self.question = question
        self.proxies = proxies
        self.proxy_flag = proxy_flag
        self.driver_flag = driver_flag
        self.less = less
    
    def begin(self, user, email, invitecode, uxlinkinfo, less):
        if self.proxy_flag == 1:  # Enable proxy pool
            driver = int_driver(self.proxies, True, less)
            
        elif self.proxy_flag == 0:  # Do not enable proxy
            proxies = "null"
            driver = int_driver(proxies, False, less)
        
        elif self.proxy_flag == 2:  # x does not use proxy, uxlink uses proxy pool
            proxy_pool = self.proxies
            proxies_x = "null"
            driver = int_driver(proxies_x, False, less)
            x = X(driver, self.url, user, email, self.passwd, self.yesclientkey, self.question)
            driver, info = x.driver_X()
            driver.quit()
            driver = int_driver(proxy_pool, True, less)
            uxuy = login_uxlink(driver, info, self.invitecode)
            uxuy.run()
            driver.quit()
            
        elif self.proxy_flag == 3:  # Use local proxy port
            driver = int_driver(self.proxies, False, less)
            
        if self.driver_flag == 1:  # Only register X
            x = X(driver, self.url, user, email, self.passwd, self.yesclientkey, self.question)
            driver, info = x.driver_X()
            driver.quit()
        elif self.driver_flag == 2:  # Only register uxlink
            # uxlinkinfo should contain info in format ['email','password','username']
            uxuy = login_uxlink(driver, uxlinkinfo, invitecode)
            uxuy.run()
            driver.quit()
        elif self.driver_flag == 3:  # Register X first, then register uxlink
            x = X(driver, self.url, user, email, self.passwd, self.yesclientkey, self.question)
            driver, info = x.driver_X()
            uxuy = login_uxlink(driver, info, invitecode)
            uxuy.run()
            driver.quit()
        elif self.driver_flag == 0:
            pass
    
    def run(self):
        try:
            user = get_random_mail()
            domains = self.domain.split(",")
            mail = random.choice(domains)
            email = user + mail
            invitecode = next(self.invitecode)
            uxlinkinfo = next(self.uxlinkinfo)
            self.begin(user, email, invitecode, uxlinkinfo, self.less)
        except Exception as e:
            print(e)

"""
proxy_flag:
    0. Do not enable proxy pool
    1. Enable proxy pool
    2. x does not use proxy, uxlink uses proxy
    3. Enter other numbers to use local proxy port
driver_flag:
    0. x does not use proxy, uxlink uses proxy
    1. Only register X
    2. Only register uxlink
    3. Register X first, then register uxlink
"""

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    proxy_flag = config.getint('Settings', 'proxy_flag')
    driver_flag = config.getint('Settings', 'driver_flag')
    proxies = config.get('Settings', 'proxies')
    invitecode = config.get('Settings', 'invitecode')
    number = config.getint('Settings', 'number')
    t = config.getint('Settings', 'thread')
    yesclientkey = config.get('Settings', 'yesclientkey')
    domain = config.get('Settings', 'domain')
    passwd = config.get('Settings', 'passwd')
    question = config.get('Settings', 'question')
    less = config.getboolean('Settings', 'less')
    
    #---------------------------------------------------------------------------------------------------#
    if driver_flag == 2:
        uxlinkinfos = eval(config.get('Settings', 'uxlinkinfo'))  # Input Twitter info list
        uxlinkinfo = iter(uxlinkinfos)
    else:
        uxlinkinfo = iter(list(range(60)))
    
    proxy = random.choice(proxies.split(","))
    
    def inviteCode_iter(invitecode, number):
        codelist = invitecode.split(",")
        code_iter = [i for i in codelist for _ in range(number)]
        random.shuffle(code_iter)
        return code_iter
    
    code_iter = inviteCode_iter(invitecode, number)
    invite_iter = iter(code_iter)
    num = math.ceil(len(code_iter) / t)
    
    for i in range(num):       
        threads = []            
        for i in range(t):
            thread = MyThread(passwd, invite_iter, domain, yesclientkey, question, proxy, uxlinkinfo, proxy_flag, driver_flag, less)
            threads.append(thread)
            thread.start()
            time.sleep(15)

        for thread in threads:  # Wait for all threads to finish
            thread.join()    
        print("All threads in this batch finished")
    print("All programs finished")     
    
main()
