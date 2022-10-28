import random
import re
import string
import sys
import time
import requests
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
import util
from names import names_list, mail_list
driver = webdriver.Chrome('./chromedriver_linux64/chromedriver')
INTERVAL = 7


class PhishingWebsite:

    # represent the URL and data about the phishing website
    def __init__(self, urlToDown):
        driver.get(urlToDown)
        self.init_password = util.generate_pass(8)
        self.init_name, self.init_mail_provider, self.init_email = util.generate_email()
        self.url = urlToDown
        self.emailField = driver.find_element(by=By.NAME, value="login_email")
        self.passwordFiled = driver.find_element(by=By.NAME, value="login_password")
        self.submitBtn = driver.find_element(by=By.NAME, value="btnLogin")
        self.data_to_send = None
        self.url_for_sign = None

    # send sample of request  to target in order to capture the request construction
    def send_sample(self):

        self.emailField.send_keys(self.init_email)
        self.passwordFiled.send_keys(self.init_password)
        self.submitBtn.click()


# handle the url and attack it
def hendler(recieved_url):
    phishing_website = PhishingWebsite(recieved_url)
    phishing_website.send_sample()
    phishing_website.data_to_send, phishing_website.url_for_sign = find_data(phishing_website)
    fill_db(phishing_website)

    driver.quit()


def find_data(phishing_website):
    for request in driver.requests:
        if request.method == 'POST' \
                and request.url.startswith(recievedURL) \
                and re.findall(phishing_website.init_name, request.body.decode("utf-8")):
            print(
                request.url,
                request.response.status_code,
                request.response.headers['Content-Type'],
                request.body
            )
            return request.body, request.url


def randonize_data(phishing_website):

    res = phishing_website.data_to_send.decode("utf-8")
    gen_name, gen_mail_provider, gen_email = util.generate_email()
    res = res.replace(phishing_website.init_name, gen_name)
    res = res.replace(phishing_website.init_mail_provider, gen_mail_provider)
    return res.encode()


def fill_db(phishing_website):

    blocked = False
    #while not blocked:
    for i in range(5):
        random_data = randonize_data(phishing_website)
        res = requests.post(phishing_website.url_for_sign, data=random_data)            #REQUST
        if not res.status_code == 200:
            blocked = True
    return blocked



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    recievedURL = sys.argv[1]
    hendler(recievedURL)

    # try:
    #     hendler(recievedURL)
    # except:
    #     print("Canot hendle")

    # Switch IP of attacker
    for i in range(5):

        util.renew_connection()
        session = util.get_tor_session()
        print(session.get("http://httpbin.org/ip").text)
        requests.get(recievedURL)
        time.sleep(INTERVAL)

    # Following prints your normal public IP
    print(requests.get("http://httpbin.org/ip").text)
