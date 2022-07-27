# This is a sample Python script.

import sys
import time
from selenium.webdriver.common.by import By
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
from selenium import webdriver
from stem import Signal
from stem.control import Controller
from webdriver_manager.chrome import ChromeDriverManager

MAX_TO_PUSH =  5
INTERVAL = 7
driver = webdriver.Chrome(ChromeDriverManager().install())

class PhishingWebsite:

    #represent the URL of phishing
    def __init__(self, urlToDown):
        driver.get(urlToDown)
        # extract correct email, password and submit button from th HTML page


        self.url = urlToDown

        self.emailField = driver.find_element(by=By.NAME, value="email")
        self.password = driver.find_element(by=By.NAME, value="password")
        self.submitBtn = driver.find_element(by=By.CLASS_NAME, value="buttonstyle")
        self.pageSource = driver.page_source

    #start attack of filling DB
    def FillDB(self):
        self.emailField.send_keys("0000000@gmail.c0m.")
        self.password.send_keys("0000000@gmail.c0m.")
        self.submitBtn.click()

    def getUserName(self):
        usernameField = re([e], self.pageSource)



# handle the url and attack it
def hendler(recievedURL):

    phishingWebsite = PhishingWebsite(recievedURL)
    phishingWebsite.FillDB()
    driver.quit()

def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session

# signal TOR for a new connection
def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="Dforce")
        # controller.authenticate()
        controller.signal(Signal.NEWNYM)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    recievedURL = sys.argv[1]
    try:
        hendler(recievedURL)
    except:
        print("Canot hendl")

    #Switch IP of attacker
    # for i in range (MAX_TO_PUSH):
    #
    #     renew_connection()
    #     session = get_tor_session()
    #     print(session.get("http://httpbin.org/ip").text)
    #     requests.get(recievedURL)
    #     time.sleep(INTERVAL)

    # Following prints your normal public IP
    print(requests.get("http://httpbin.org/ip").text)






