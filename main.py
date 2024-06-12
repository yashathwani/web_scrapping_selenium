import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time




PATH = r"C:\webdrivers\chromedriver.exe"
service = Service(PATH)
options = Options()
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.youtube.com/watch?v=DyDfgMOUjCI")
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="comments"]')))


def scroll_and_print_comments(drivers):
    last_height = drivers.execute_script("return document.documentElement.scrollHeight")
    loaded_comments = set()

    while True:
        drivers.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)

        comment_elements = drivers.find_elements(By.CSS_SELECTOR, 'yt-attributed-string#content-text')
        for element in comment_elements:
            comment_text = element.text
            if comment_text not in loaded_comments:
                print(comment_text)
                loaded_comments.add(comment_text)

        new_height = drivers.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


scroll_and_print_comments(driver)

driver.quit()
