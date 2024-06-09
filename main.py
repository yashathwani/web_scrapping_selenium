from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

PATH = r"C:\webdrivers\chromedriver.exe"
service = Service(PATH)
options = Options()
driver = webdriver.Chrome(service=service,options=options)
driver.get("https://www.youtube.com/watch?v=q9A-CVILK4g")
time.sleep(5)
element = driver.find_element(By.CSS_SELECTOR, 'yt-formatted-string.style-scope.ytd-watch-metadata')
text=element.text
print(text)
driver.quit()
