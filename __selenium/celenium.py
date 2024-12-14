from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
import os
import time
import requests


class S_Testing:
    
    def __init__(self):
        self.driver = None
        # Initialize the WebDriver
        self.driver = webdriver.Chrome()
        


    def Register(self):
        try:
            #Username
            self.driver.get("http://10.0.0.14:8080/registerPage")
            r_username = self.driver.find_element(By.NAME, "username")
            r_username.send_keys("Test111")
            #Password
            r_password = self.driver.find_element(By.NAME, "password")
            r_password.send_keys("Test111")
            #Submit
            time.sleep(5)
            reg_submit = self.driver.find_element(By.ID, "reg-btn")
            reg_submit.click()
            time.sleep(5)
            alert = Alert(self.driver)
            alert.accept()
        finally:
            self.Login()
            
    def Login(self):
        try:    
            # Find the form element
                
            # Find username and password fields for login
            self.driver.execute_script("""
            let currentUrl = window.location.href;
            let baseUrl = currentUrl.split('?')[0];
            window.location.replace(baseUrl);
            """)
            l_username = self.driver.find_element(By.NAME, "username")
            l_username.send_keys("Test111")
            l_password = self.driver.find_element(By.NAME, "password")
            l_password.send_keys("Test111")                
            log_submit = self.driver.find_element(By.ID, "login-btn")
            log_submit.click()                
            time.sleep(5)  # Wait for the backend to process the request and give a response
            alert = Alert(self.driver)
            alert.accept()  # If there's an alert, we accept it (successful login, etc.)
            time.sleep(5)
        except Exception as e:
            print("Error during login:", e)

        finally:
            self.addDomain()

    def addDomain(self):
        add = self.driver.find_element(By.ID, "addDomainBtn")
        add.click()
        submit = self.driver.find_element(By.CLASS_NAME, "submit-btn")
        add_domain = self.driver.find_element(By.ID, "domainName")
        add_domain.send_keys("bibi.com")
        time.sleep(10)
        submit.click()
        time.sleep(100)



test = S_Testing()

test.Register()
