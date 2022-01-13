from explicit import waiter, XPATH
from src.service.credentials import TWITTER_PASSWORD, TWITTER_USERNAME
import random
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.common.by import By
import undetected_chromedriver.v2 as uc
import selenium
import datetime
from bs4 import BeautifulSoup
import numpy as np
import os
from src.service.client_mongodb import ClientDB

class TwitterScraper:
    def __init__(self, headless=False, download_path="", date=False, account=False):
        self.client_db = ClientDB()
        self.base_dir = f"{os.path.dirname(os.path.realpath(__file__))}/selenium_modules/"
        self.date = date
        self.account = account
        try:
            self.driver = self.__driver(headless, download_path)
            print(self.driver.execute_script("return navigator.userAgent"))

        except selenium.common.exceptions.InvalidArgumentException as e:
            time.sleep(5)
            print("Retrying")
            self.__init__()

        self.authentication()

    def __driver(self, headless, download_path):
        options = uc.ChromeOptions()
        options.user_data_dir = f"{self.base_dir}chrome_profile/"
        options.add_argument(f"--user-data-dir={self.base_dir}chrome_profile/")
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        # prefs = {
        # "translate_whitelists": {"your native language":"en"},
        # "translate":{"enabled":"True"}
        # }
        # options.add_experimental_option("prefs", prefs)
        # options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})

        # if download_path:
        #     options.add_experimental_option("prefs", {
        #         "download.default_directory": download_path,
        #         "download.prompt_for_download": False,
        #         "download.directory_upgrade": True,
        #         "safebrowsing.enabled": True
        #     })

        if headless:
            options.headless=True
            options.add_argument("--headless")
        else:
            print(self.base_dir)
            options.add_extension(f'{self.base_dir}idontcareaboutcookies.crx')

        return uc.Chrome(executable_path=f"{self.base_dir}/chromedriver", options=options, version_main=95)


    def get_accounts(self):
        users_collection = [user["name"] for user in self.client_db.get_collection("influent_bitcoin_account")]
        res = []
        for user in users_collection:
            if user.startswith("@"):
                user = user[1:]

            res.append(user)

        return res

    def simulate_human_input(self, element, keys):
        for key in keys:
            element.send_keys(key, Keys.ARROW_DOWN)
            time.sleep(random.uniform(0.15, 0.65))

    def login(self):
        self.driver.get("https://twitter.com/i/flow/login")
        username_input = WebDriverWait(self.driver, 60).until(lambda x: x.find_element(By.XPATH, "//input[@autocomplete='username']"))
        self.simulate_human_input(username_input, TWITTER_USERNAME)
        waiter.find_element(self.driver, "//span[text()='Next'] | //span[text()='Suivant']", by=XPATH).click()

        try:
            WebDriverWait(self.driver, 3).until(lambda x: x.find_element(By.XPATH, "//span[contains(text(), 'There was unusual login activity on your account.')]"))
            text_input = WebDriverWait(self.driver, 10).until(lambda x: x.find_element(By.XPATH, "//input[@name='text']"))
            self.simulate_human_input(text_input, TWITTER_USERNAME)
            waiter.find_element(self.driver, "//span[text()='Next'] | //span[text()='Suivant']", by=XPATH).click()

        except selenium.common.exceptions.TimeoutException:
            pass
        password_input = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath("//input[@name='password']"))
        self.simulate_human_input(password_input, TWITTER_PASSWORD)
        WebDriverWait(self.driver, 10).until(lambda x: x.find_element(By.XPATH, "//span[text()='Log in'] | //span[text()='Se connecter']")).click()
        WebDriverWait(self.driver, 2)

    def authentication(self):
        self.driver.get("https://twitter.com")
        if self.driver.current_url.endswith("home"):
            self.is_authenticated = True
        else:
            self.login()

    def generate_url(self, keywords, min_faves, min_retweets, min_replies, lang, step, since="", account=""):
        if self.date:
            until = (datetime.datetime.strptime(since, "%Y-%m-%d") + datetime.timedelta(days=step)).strftime("%Y-%m-%d")
            url = f"https://twitter.com/search?q={keywords} min_faves:{min_faves} min_retweets:{min_retweets} min_replies:{min_replies} since:{since} until:{until} lang:{lang}"
            return url, until
        elif self.account:
            url = f"https://twitter.com/search?q={keywords} min_faves:{min_faves} min_retweets:{min_retweets} min_replies:{min_replies} since:{since} from:{account} lang:{lang}"
            print(url)
            return url

    def scroll_to(self, start, stop):
        for l in np.arange(start, stop, random.uniform(2, 5)): ##slow scroll through product page
            self.driver.execute_script("window.scrollTo(0, {});".format(l))
        
    def crawl_historical_tweets(self, keywords, lang="en", min_faves=1000, min_retweets=280, min_replies=50, since="2019-01-01", to="now", account="", step=2):
        if to == "now":
            to = datetime.datetime.now().strftime("%Y-%m-%d")
        
        to_obj = datetime.datetime.strptime(to, "%Y-%m-%d")
        until = datetime.datetime.strptime(to, "%Y-%m-%d") - datetime.timedelta(days=step)

        users = self.get_accounts()
        i = 0

        while until < to_obj or i <= len(users)-1:
            if self.date:
                url, since = self.generate_url(keywords, min_faves, min_retweets, min_replies, lang, 1, since)
            elif self.account:
                url = self.generate_url(keywords, min_faves, min_retweets, min_replies, lang, 1, since=since, account=users[i])
                print(i, len(users))
                i += 1
            self.driver.get(url)

            reached_page_end = False
            last_height = self.driver.execute_script("return document.body.scrollHeight")            
            self.scroll_to(0, last_height+1)
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            while not reached_page_end:
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                [s.decompose() for s in soup("script")]  # remove <script> elements
                try:
                    tweets = self.extract_tweets(soup, account=users[i]) if self.account else self.extract_tweets(soup)
                    print(tweets)
                    if len(tweets):
                        self.insert_to_db(tweets)
                    time.sleep(1)

                    self.scroll_to(last_height, new_height)
                    new_height = self.driver.execute_script("return document.body.scrollHeight")

                    if last_height == new_height:
                        reached_page_end = True
                    else:
                        last_height = new_height
                except Exception as e:
                    print(e)
                    reached_page_end = True


    def extract_tweets(self, soup, account=""):
        tweets = soup.find_all("div", {"class": "css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"})#A modifier
        res = []
        print(len(tweets))
        for tweet in tweets:
            text_div = tweet.find("div", {"class": "css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0"})
            user_div = tweet.find("div", {"class": "css-901oao r-1awozwy r-18jsvk2 r-6koalj r-37j5jr r-a023e6 r-b88u0q r-rjixqe r-bcqeeo r-1udh08x r-3s2u2q r-qvutc0"})
            reply = tweet.find("div", {"data-testid": "reply"})["aria-label"].split(" ")[0]
            retweet = tweet.find("div", {"data-testid": "retweet"})["aria-label"].split(" ")[0]
            like = tweet.find("div", {"data-testid": "like"})["aria-label"].split(" ")[0]

            text_span = text_div.find_all("span")
            user_span = user_div.find("span", {"class": "css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"})

            tweet_datetime = tweet.find("time")["datetime"]

            text = ""
            user = ""

            for span in text_span:
                text += span.text

            for span in user_span:
                user += span.text

            if self.account:
                user = account

            res.append({"dt": tweet_datetime, "user": user, "text": text, "like": like, "retweet": retweet, "reply": reply})
        return res

    def insert_to_db(self, tweets):
        self.client_db.insert_documents("tweets", tweets)
        

if __name__ == "__main__":
    test = TwitterScraper(headless=False)
    test.crawl_historical_tweets("bitcoin", min_faves=100, min_retweets=28, min_replies=0, since="2021-01-01", to="now", step=2)

