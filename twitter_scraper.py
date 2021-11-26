from scraper import Scrap
from explicit import waiter, XPATH
from credentials import TWITTER_PASSWORD, TWITTER_USERNAME
import random
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.common.by import By
import selenium

class TwitterScraper:
    def __init__(self):
        self.scraper = Scrap(remote=False, headless=False)
        self.driver = self.scraper.get_driver()

    def simulate_human_input(self, element, keys):
        for key in keys:
            element.send_keys(key, Keys.ARROW_DOWN)
            time.sleep(random.uniform(0.15, 0.65))

    def login(self):
        self.driver.get("https://twitter.com/i/flow/login")
        # waiter.find_element(self.driver, "//span[text()='Sign in']", by=XPATH).click()
        # time.sleep(0.3)
        # waiter.find_element(self.driver, "//span[text()='Use your phone number, email address or username']", by=XPATH).click()

        username_input = WebDriverWait(self.driver, 10).until(lambda x: x.find_element(By.XPATH, "//input[@name='username']"))
        self.simulate_human_input(username_input, TWITTER_USERNAME)
        waiter.find_element(self.driver, "//span[text()='Next']", by=XPATH).click()

        try:
            WebDriverWait(self.driver, 3).until(lambda x: x.find_element(By.XPATH, "//span[contains(text(), 'There was unusual login activity on your account.')]"))
            text_input = WebDriverWait(self.driver, 10).until(lambda x: x.find_element(By.XPATH, "//input[@name='text']"))
            self.simulate_human_input(text_input, TWITTER_USERNAME)
            waiter.find_element(self.driver, "//span[text()='Next']", by=XPATH).click()

        except selenium.common.exceptions.TimeoutException:
            pass

        password_input = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath("//input[@name='password']"))
        self.simulate_human_input(password_input, TWITTER_PASSWORD)
        WebDriverWait(self.driver, 10).until(lambda x: x.find_element(By.XPATH, "//span[text()='Log in']")).click()
        time.sleep(5)

    def get(self):
        self.driver.get("https://twitter.com")
        time.sleep(10)

if __name__ == "__main__":
    test = TwitterScraper()
    # test.login()
    test.get()

