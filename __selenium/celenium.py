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
            ## TO DO > Find a way to get Alert context in order to know if to proceed login
        finally:
            pass
            
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
        ## TO DO > Find a way to get Alert context in order to know if to proceed login
        finally:
            pass

    def addDomain(self):
        add = self.driver.find_element(By.ID, "addDomainBtn")
        add.click()
        submit = self.driver.find_element(By.CLASS_NAME, "submit-btn")
        add_domain = self.driver.find_element(By.ID, "domainName")
        add_domain.send_keys("rakbibi.com")
        time.sleep(5)
        submit.click()
        time.sleep(5)
    
    def domainBulk(self):
        file_path = os.path.abspath('__selenium/100domains.txt')
        add = self.driver.find_element(By.ID, "addDomainBtn")
        add.click()
        bulk_button = self.driver.find_element(By.ID,"domainsFile")
        time.sleep(10)
        bulk_button.send_keys(file_path)
        time.sleep(5)
        submit = self.driver.find_element(By.CLASS_NAME, "submit-btn")
        submit.click()
        time.sleep(10)
    
    def logout(self):
        logout = self.driver.find_element(By.CLASS_NAME, "logout")
        logout.click()
        time.sleep(10)


    def zeroToHero(self):
        self.Register()
        self.Login()
        self.addDomain()
        self.domainBulk()
        self.logout()
        self.driver.quit()
    ##TO DO > Check if need to create a variable that is in charge of  self.driver.quit or not
        





test = S_Testing()

test.zeroToHero()

