
import re
import sys
import threading
import time
import requests
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

import page_detales
import util
driver = webdriver.Chrome('./chromedriver_linux64/chromedriver')
TOR_INTERVAL = 7
PASSWORDS_LEN = 8
THREADS_NUM = 5


class PhishingWebsite:

    # represent the URL and data about the phishing website
    def __init__(self, urlToDown):
        driver.get(urlToDown)
        self.init_password = util.generate_pass(PASSWORDS_LEN)
        self.init_name, self.init_mail_provider, self.init_email = util.generate_email()
        self.url = urlToDown
        self.emailField = driver.find_element(by=By.NAME, value=page_detales.fileds_names["user_name"])
        self.passwordFiled = driver.find_element(by=By.NAME, value=page_detales.fileds_names["password"])
        self.submitBtn = driver.find_element(by=By.NAME, value=page_detales.fileds_names["submit_button"])
        self.data_to_send = None
        self.url_for_sign = None

    # send sample of request  to target in order to capture the request construction
    def send_sample(self):

        self.emailField.send_keys(self.init_email)
        self.passwordFiled.send_keys(self.init_password)
        self.submitBtn.click()


# handle the url and attack it
def hendler(recieved_url):
    for i in range(5):
        phishing_website = PhishingWebsite(recieved_url)
        phishing_website.send_sample()
        driver.quit()
    phishing_website.data_to_send, phishing_website.url_for_sign = find_data(phishing_website)
    #send_threads(fill_db, phishing_website, THREADS_NUM)
    fill_db(phishing_website)
    driver.quit()


def find_data(phishing_website):
    for request in driver.requests:
        if request.method == 'POST' \
                and request.url.startswith(recievedURL) \
                and re.findall(phishing_website.init_name, request.body.decode("utf-8")):
            print(
                "Sample of first packet sent:\n",
                request.url,
                request.response.status_code,
                request.response.headers['Content-Type'],
                request.body
            )
            return request.body, request.url


def randonize_data(phishing_website):

    res = phishing_website.data_to_send.decode("utf-8")
    random_name, random_provider, random_email = util.generate_email()
    random_password = util.generate_pass(PASSWORDS_LEN)
    res = res.replace(phishing_website.init_name, random_name)
    res = res.replace(phishing_website.init_mail_provider, random_provider)
    res = res.replace(phishing_website.init_password, random_password)
    return res.encode(), random_email, random_password


def fill_db(phishing_website):

    random_data, email, password = randonize_data(phishing_website)
    res = requests.post(phishing_website.url_for_sign, data=random_data)  # REQUST
    print("Send email: {} with passowrd: {}".format(email, password))

    # blocked = False
    # while not blocked:
    #     random_data, email, password = randonize_data(phishing_website)
    #     res = requests.post(phishing_website.url_for_sign, data=random_data)            #REQUST
    #     print("Send email: {} with passowrd: {}".format(email, password))
    #     if not res.status_code == 200:
    #         blocked = True
    # return blocked


def send_threads(function, arg, threads_num):

    theads = []
    for i in range(threads_num):
        t = threading.Thread(target=fill_db, args=(arg,), daemon=True)
        theads.append(t)

    for i in range(threads_num):
        theads[i].start()

    for i in range(threads_num):
        theads[i].join()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # try:
    recievedURL = "http://localhost/wordpress/log-in/"
    #recievedURL = input("PLease insert URL for attack\n")
    hendler(recievedURL)

    #     driver.quit()
    # except Exception as e:
    #     print("Canot hendle because:", e.__class__)

    # Switch IP of attacker
    # for i in range(5):
    #
    #     util.renew_connection()
    #     session = util.get_tor_session()
    #     print(session.get("http://httpbin.org/ip").text)
    #     requests.get(recievedURL)
    #     time.sleep(TOR_INTERVAL)

    # Following prints your normal public IP
    print(requests.get("http://httpbin.org/ip").text)
