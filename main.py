from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# initiate a chrome driver
ser = Service("D:\chromedriver_win32\chromedriver.exe")
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)


URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.65580214453125%2C%22east%22%3A-122.21085585546875%2C%22south%22%3A37.56005507446884%2C%22north%22%3A37.989903032322125%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfr2cTsuw2RrcuQtOumduPfI7fe2d_g4begglNnQ06tnzZbfg/viewform?usp=sf_link"

driver.get(URL)
time.sleep(4)

# click tab 20 times to go to the listing section
# then scroll down to fetch all the listing data
for _ in range(20):
    webdriver.ActionChains(driver).key_down(Keys.TAB).perform()
for _ in range(120):
    webdriver.ActionChains(driver).key_down(Keys.ARROW_DOWN).perform()

html_data = driver.page_source
soup = BeautifulSoup(html_data, "html.parser")


# Get the price:
price_list = [price.text.split("/")[0].split("+")[0].replace("$", "").split(" ")[0] for price in soup.select(".list-card-heading .list-card-price")]
# Get the address list:
address_list = [address.getText() for address in soup.find_all(name="address", class_="list-card-addr")]
# Get the link:
link_list = [link.get("href") for link in soup.select(".list-card-info .list-card-link")]


for i in range(len(price_list)):
    driver.get(GOOGLE_FORM_URL)
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(f"{address_list[i]}")
    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(f"{price_list[i]}")
    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(f"{link_list[i]}")
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span').click()


driver.quit()