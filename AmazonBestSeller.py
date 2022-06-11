from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

driver = webdriver.Chrome(r"C:\Users\Divyansh\Downloads\chromedriver_win32\chromedriver.exe")


def get_data(pageno):
    url = ('https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_' + str(pageno) + '?ie=UTF8&pg=' + str(pageno))
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')
    all = []
    second_links = []
    temp = soup.find_all('span', class_="aok-inline-block zg-item")
    for curr in temp:
        alink = curr.find('a')
        second_links.append("https://www.amazon.in" + alink.get('href'))
    for i in range(0, len(second_links)):
        url = str(second_links[i])
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, 'lxml')
        details = soup.find('div', id="detailBullets_feature_div")
        lis = details.find_all('li')
        final_list = []
        all1 = []
        for curr in lis:
            combined = curr.text.replace("\n", "").split('\u200f:\u200e')
            combined = [x.strip() for x in combined]
            final_list.append(combined)
        c = 0
        while True:
            if final_list[i][0] == "Publisher" or "Language" or "Paperback" or "ISBN-10" or "ISBN-13" or "Item Weight" or "Dimensions":
                temp_list = final_list[i][1].split("(")
                temp_list = temp_list[0]
                c += 1
            if c > 7:
                break
            if temp_list == "":
                all1.append("Unknown")
            else:
                all1.append(temp_list)
            i += 1
        cust_review = ""
        details = soup.find_all('div',
                                class_="a-expander-content reviewText review-text-content a-expander-partial-collapse-content")
        c = 1
        for curr in details:
            if c > 3:
                break
            temp = curr.text
            temp = temp.rstrip()
            temp = temp.lstrip()
            cust_review += str(c) + "." + temp + "\n"
            c += 1
        all1.append(cust_review)
        all.append(all1)
    return all


results = []
no_pages = 1
for i in range(1, no_pages + 1):
    results.append(get_data(i))
flatten = lambda l: [item for sublist in l for item in sublist]
df = pd.DataFrame(flatten(results),
                  columns=['Publisher', 'Language', 'Paperback', 'ISBN_10', 'ISBN_13', 'Weight', 'Dimensions',
                           'Cust_Review'])
print(df)
