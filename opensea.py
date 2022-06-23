from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd


def save_to_local(tran_list: list):
    df = pd.DataFrame(tran_list, columns=['slug'])
    df.to_csv(path_or_buf='./nft_slug.csv', index=False)


def fetch_slug(chrome_driver):
    collection_links = []
    content = BeautifulSoup(chrome_driver.page_source, 'html.parser')
    for a in content.find_all('a', href=True):
        if '/collection/' in a['href']:
            collection_links.append(a['href'])
    return collection_links


def scroll_and_fetch(chrome_driver, height=0, count=0, collection_slug_list=[]):
    total_height = int(chrome_driver.execute_script("return document.body.scrollHeight"))
    scroll_height = int(total_height / 20)

    chrome_driver.execute_script("window.scrollTo(0, {});".format(1))  # Start at top
    time.sleep(6)
    for i in range(1, total_height, scroll_height):
        collection_slug_list.extend(fetch_slug(chrome_driver))
        chrome_driver.execute_script("window.scrollTo(0, {});".format(i))  # Scroll to bottom

    new_height = int(driver.execute_script("return document.body.scrollHeight"))
    print("actual height: %d" % new_height)

    count += 1
    if count < 100:
        chrome_driver.find_element(By.XPATH, '//*[@id="main"]/div/div[3]/button[2]').click()  # next page
        scroll_and_fetch(chrome_driver, 0, count, collection_slug_list)
    else:
        print("end of scroll. Number of pages: %d" % count)
        print(len(set(collection_slug_list)))
        print(set(collection_slug_list))
        collection_slug_list = list(set(collection_slug_list))
        save_to_local(collection_slug_list)
        return collection_slug_list


if __name__ == '__main__':
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.get('https://opensea.io/rankings?sortBy=total_volume')
    scroll_and_fetch(driver)
    input("press enter to quit")
    driver.quit()
