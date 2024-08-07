from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from random import *
from api import *
from datetime import datetime
import string
import zipfile
import requests
import random
import time
import os
import re
import json
import base64
import uuid


def create_proxy_auth_extension(proxy_host, proxy_port, proxy_username, proxy_password, scheme='http',
                                plugin_path=None):
    if plugin_path is None:
        plugin_path = 'proxy/{}_{}@http-dyn.dobel.com_9020.zip'.format(proxy_username, proxy_password)

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Dobel Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = string.Template(
        """
        var config = {
            mode: "fixed_servers",
            rules: {
                singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                },
                bypassList: ["foobar.com"]
            }
          };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
        );
        """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )

    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path

# Parse proxy information
def from_proxy_get_daili(proxy):
    # proxy is in the format user:pass@ip:port
    user_pass_str, ip_port_str = proxy.split('@')
    proxyHost, proxyPort = ip_port_str.split(':')
    proxyUser, proxyPass = user_pass_str.split(':')
    return proxyHost, proxyPort, proxyUser, proxyPass

# Initialize the browser
def int_driver(proxy, flag=False, headless=False):
    options = webdriver.ChromeOptions()
    # Default to not enable browser authentication proxy
    if flag == True:
        options.add_extension(proxy_auth_plugin_path)
        proxyHost, proxyPort, proxyUser, proxyPass = from_proxy_get_daili(proxy)
        proxy_auth_plugin_path = create_proxy_auth_extension(
            proxy_host=proxyHost,
            proxy_port=proxyPort,
            proxy_username=proxyUser,
            proxy_password=proxyPass)   
    elif proxy.split(":")[0] == "127.0.0.1":
        options.add_argument(f'--proxy-server={proxy}')
    options.add_experimental_option("excludeSwitches", ["enable_automatin"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features-AutomationControlled")
    driver = webdriver.Chrome(options=options)
    if headless == True:
        # options.add_argument("--headless")
        driver.set_window_position(-2000, 0)
    # Move the browser off-screen
    return driver


# Register on Twitter
class X:
    def __init__(self, driver, url, user, email, passwd, yesclientkey, question):
        self.driver = driver
        self.url = url
        self.user = user
        self.email = email
        self.passwd = passwd
        self.yesclientkey = yesclientkey
        self.question = question
        
    # Switch window to frame
    def frame_switch(self, driver):
        wait = WebDriverWait(driver, 10)
        iframe1 = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='arkoseFrame']")))
        driver.switch_to.frame(iframe1)
        iframe2 = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='arkose']/div/iframe")))
        driver.switch_to.frame(iframe2)
        iframe3 = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='game-core-frame']")))
        driver.switch_to.frame(iframe3)
        return driver

    Here is the updated code with all comments translated into English:

# Specific operations for Twitter registration
    def signup(self, driver, url, user, email, passwd):
        driver.get(url)
        wait = WebDriverWait(driver, 8)
        print("Creating account, please wait 30 seconds")
        time.sleep(2.5)
        # Create account
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]"))).click()

        # Enter username
        print("Entering username")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/label/div/div[2]/div/input"))).send_keys(user)

        # Switch to email registration
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/button"))).click()
        except Exception as e:
            print("This IP is invalid, please try another one")

        # Enter email
        print("Entering email")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/label/div/div[2]/div/input"))).send_keys(email)

        # Select birthday
        print("Selecting birthday")
        selects = driver.find_elements(By.TAG_NAME, 'select')
        time.sleep(0.3)
        option1 = Select(selects[0])
        option1.select_by_value(str(randint(1, 12)))
        time.sleep(0.3)
        option1 = Select(selects[1])
        option1.select_by_value(str(randint(1, 28)))
        time.sleep(0.3)
        option1 = Select(selects[2])
        option1.select_by_value(str(randint(1990, 2005)))
        time.sleep(0.5)

        # Perform email verification
        print("Performing email verification")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button"))).click()

        time.sleep(2)
        # Start CAPTCHA verification
        print("Performing CAPTCHA verification")
        # Switch to frame window

        time.sleep(2)
        driver = self.frame_switch(driver)   # Switch frame

        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='root']/div/div[1]/button"))).click()  # Click verification button
        time.sleep(2)
        # Get blob image
        i = 0
        last_url = "global_img_url" # Use closure
        while True:
            try:  # Exit loop if this page does not exist
                driver.find_elements(By.XPATH, "//*[@id='game-core-frame']")
            except:
                print("Verification finished")
                break
            try:
                print(f"Attempt {i + 1}")
                name = user + str(i)
                # Perform CAPTCHA resolution
                def capt():
                    nonlocal last_url
                    cap = Captcha(driver, self.yesclientkey, name, self.question)
                    last_url = cap.run(last_url)
                    return last_url
                last_url = capt()
                i += 1
            except Exception as e:
                print("Error", e)
                break
        print("CAPTCHA verification completed")  
        # Get verification code

        # Switch browser back to the original window
        driver.switch_to.default_content()
        print("Getting verification code")
        time.sleep(8)
        validation_code = get_code(email)

        time.sleep(1)
        # Enter verification code
        print("Entering verification code")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input"))).send_keys(validation_code)

        time.sleep(1)
        # Next step
        print("Next step")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button"))).click()

        time.sleep(1)
        # Enter password
        print("Entering password")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div/label/div/div[2]/div[1]/input"))).send_keys(passwd)

        time.sleep(2)
        # Register button
        print("Register button")                                  
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div[2]/button/div/span/span"))).click()

        time.sleep(1.5)
        # Proceed to personal information completion
        print("Proceeding to personal information completion")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button"))).click()

        # Choose name
        print("Choosing name")
        try:
            el = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')))
            name = el.get_attribute("value")
        except:
            name = "Not found"
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button"))).click()

        # Skip notifications
        print("Skipping notifications")
        time.sleep(1.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div/div/div[2]/div[2]/button[2]"))).click()

        # Choose interests
        print("Choosing interests")
        time.sleep(1.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Music')]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Food')]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Sports')]"))).click()

        # Next step
        print("Next step")
        time.sleep(1.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/button"))).click()

        # Next step
        print("Next step")
        time.sleep(0.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/button"))).click()

        # Follow
        print("Following")
        time.sleep(0.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/section/div/div/div[3]/div/div/button/div/div[2]/div/div[2]/button"))).click()

        # Next step
        print("Next step")
        time.sleep(0.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button"))).click()

        time.sleep(1.5)
        return name, driver

    # Execute X
    def driver_X(self):
        """ 
        :return : driver: Browser instance
                : [email, passwd, name]: Information list
        """
        ip = get_ip(self.driver)
        print(ip)
        flag = False
        try:
            name, driver = self.signup(self.driver, self.url, self.user, self.email, self.passwd)
            print("Registration successful!")
            flag = True
        except Exception as e:
            print("Registration failed!", e)
    
        if flag:
            print(f"Username: {name}, Email: {self.email}, Password: {self.passwd}, IP: {ip}")
            with open('twitter.log', 'a') as f:
                writetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Record time
                f.write(f"['{self.email}', '{self.passwd}', '{name}']    |   IP:{ip}, time:{writetime}\n----------------------------------------------------------------\n")
            return driver, [self.email, self.passwd, name]
        else:
            return None, [None, None, None]

        
# Anti-bot CAPTCHA recognition
class Captcha:
    def __init__(self, driver, clientKey, name, question):
        self.driver = driver
        self.clientKey = clientKey
        self.name = name
        self.question = question
        
    def create_task(self) -> str:
        """ 
        Step 1: Create a CAPTCHA task 
        :param 
        :return taskId : string ID of the created task
        """
        #base64_str=self.png_to_base64(f"img/{self.name}.png")
        url = "https://api.yescaptcha.com/createTask"
        data = {
            "clientKey": self.clientKey,
            "task": {
                "type": "FunCaptchaClassification",
                "image": self.base64_dec_img,
                "question": f"{self.question}",
                "softID": 46487
            }
        }
        result = requests.post(url, json=data, verify=False).json()
        taskId = result.get('taskId')
        return taskId
        
    def get_response(self, taskId) -> int:
        url = 'https://api.yescaptcha.com/getTaskResult'
        data = {
            "clientKey": self.clientKey,
            "taskId": taskId
        }
        num = requests.post(url, json=data, verify=False).json()['solution']['objects']
        print(f"The correct one is image {num[0] + 1}")
        return num[0]
    
    # Simulate click operations
    def verify_website(self, num):
        if num > 0:  # Click only if num > 0, otherwise, it's the first image, no click needed
            for i in range(num):
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='root']/div/div[1]/div/div/div[2]/div[1]/a[2]"))).click()
        else:
            time.sleep(uniform(0.1, 0.2))
        # Click submit
        self.driver.find_element(By.XPATH, "//*[@id='root']/div/div[1]/div/button").click()
    
    # Get image URL
    def get_img_url(self):
        img_element = self.driver.find_element(By.XPATH, "//*[@id='root']/div/div[1]/div/div/div[2]/div[1]/img")
        img = img_element.get_attribute('style')
        blob = re.findall(r'background-image: url\("(.*?)"\);', img)[0]
        print(blob)
        return blob
    
    # Save the verification image
    def save_img(self, blob):
        # Call function and get base64 encoding
        data_url = self.driver.execute_async_script("""
        var callback = arguments[arguments.length - 1];
        function get_base64(url) {
            return new Promise((resolve, reject) => {
                var img = new Image();
                img.setAttribute('crossOrigin', 'anonymous');
                img.onload = function() {
                    var canvas = document.createElement('canvas');
                    canvas.width = this.naturalWidth;
                    canvas.height = this.naturalHeight;
                    var ctx = canvas.getContext('2d');
                    ctx.drawImage(this, 0, 0);
                    resolve(canvas.toDataURL('image/png'));
                };
                img.onerror = reject;
                img.src = url;
            });
        }
        get_base64(arguments[0]).then(callback).catch(callback);
        """, blob)
        # Decode and save the image
        self.base64_dec_img = data_url
        """ if data_url:
            self.base64_to_png(data_url, f"img/{self.name}.png")   # To be developed
            print("Image saved successfully")
        else:
            print("Image save failed") """
    
    # Convert image to base64
    def png_to_base64(self, file_path):
        with open(file_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read())
            return "data:image/png;base64," + encoded_image.decode('utf-8')

    # Restore PNG image from Base64 encoding
    def base64_to_png(self, base64_str, output_path):
        image_data = base64.b64decode(base64_str.split(',')[1])
        with open(output_path, "wb") as output_file:
            output_file.write(image_data)
     
    def run(self, last_url):
        img_url = self.get_img_url()
        # Keep accessing until a new one appears
        while img_url == last_url:
            try:
                time.sleep(1)
                img_url = self.get_img_url()
            except Exception as e:
                if isinstance(e, NoSuchElementException):
                    print("No element found, ending")
                    break  # Exit the loop
                else:
                    print(f"An unexpected error occurred: {e}")
        last_url = img_url
        print("Recorded URL", last_url)
        self.save_img(img_url)
        while True:
            try:
                taskId = self.create_task()
                num = self.get_response(taskId)
                break
            except Exception as e:
                print("Retrying request:", e)  
        self.verify_website(num)
        return last_url  

# Get browser IP
def get_ip(driver):
    try:
        driver.get('http://httpbin.org/ip')
        res = str(driver.page_source)
        ip = re.findall(r'"origin": "(.*?)"', res)[0]
    except Exception as e:
        ip = "127.0.0.1"
        print("Error getting IP:", e)
    return ip


# Registering for UXLink
class LoginUXLink:
    def __init__(self, driver, info, invitecode):
        self.driver = driver
        self.email = info[0]
        self.password = info[1]
        self.username = info[2]
        self.invitecode = invitecode
        self.wait = WebDriverWait(self.driver, 6)
        
    def get_AuthURL(self):
        _uuid = uuid.uuid4()
        headers = {
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "Referer": "https://dapp.uxlink.io/",
        }
        url = 'https://api.uxlink.io/activity/twitter/getAuthenURL'
        data = {
            "refType": 2,
            "inviteCode": f"{self.invitecode}",
            "callbackPath": f"/authGateway?routerPath=/?inviteCode={self.invitecode}",
            "sign": f"{_uuid}"
        }
        authenURL = requests.post(url, json=data, headers=headers).json()['data']['authenURL']
        return authenURL
    
    # Get login verification code
    def get_verify_code(self):
        resp = requests.get(f"http://xxxx.top:8080/new?email={self.email}")
        code = resp.json()['title'].split(" ")[-1]
        print(code)
        return code
    
    def login(self):
        url = self.get_AuthURL()
        ip = get_ip(self.driver)
        print(ip)
        wait = self.wait
        self.driver.get(url)
        
        # Enter email
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input"))).send_keys(self.email)
        # Next step
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]/div/span/span"))).click()
        
        # If account is abnormal
        try:
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input"))).send_keys(self.username)
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button/div/span/span"))).click()
        except Exception as e:
            print(e)
        
        # Enter password
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input"))).send_keys(self.password)
        
        # Login
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button/div/span/span"))).click()
        
        # Account abnormality setting: Get verification code
        # First method
        try:
            time.sleep(5)
            verify_code = self.get_verify_code()
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input"))).send_keys(verify_code)
            # Next step
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button/div"))).click()
        except Exception as e:
            print(e)
        
        # Authorization
        time.sleep(1.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div[2]/div/div/div[1]/div[3]/button/div/span/span"))).click()
        time.sleep(20)
        
        # Get invitation code
        try:
            self.driver.get("https://dapp.uxlink.io/my")
            time.sleep(3)
            element = self.driver.find_element(By.XPATH, "//*[@id='app']/div/div[3]/div/div[2]/div[1]/div[2]/div[1]/span[2]")
            invite = element.text
            print("Invitation code:", invite)
        except:
            invite = "null"
        
        with open("uxlink.log", 'a') as f:
            writetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Record time
            f.write(f"{self.invitecode}     |    {self.email}   |   invitecode:{invite}   |   ip:{ip}  |  {writetime}\n-----------------------------------------------------------------------------------\n")
        
        print("Registration successful")
        
    def run(self):
        self.login()

