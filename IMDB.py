import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import chain
from selenium import webdriver

driver = webdriver.Chrome(r"C:\Users\Divyansh\Downloads\chromedriver_win32\chromedriver.exe")

def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele
    str1 = str1[:-1]
    return str1


def get_data(page):
    url = "https://www.imdb.com/search/title/?release_date=2020-01-01,2020-12-31&sort=num_votes,desc&start="+str(1+(page-1)*50)+"&ref_=adv_nxt"
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')

    all = []
    movieFrame = soup.find_all('div', class_="lister-item-content")
    for movie in movieFrame:
        all1 = []
        movieDirector = []
        movieStars = []
        movieFirstLine = movie.find("h3", class_="lister-item-header")
        all1.append(movieFirstLine.find("a").text)
        if movie.find("strong") is not None:
            all1.append(movie.find("strong").text)
        else:
            all1.append("Unknown")
        all1.append(movie.find_all("p", class_="text-muted")[-1].text.lstrip())
        movieNumbers = movie.find_all("span", attrs={"name": "nv"})
        if len(movieNumbers) == 2 or len(movieNumbers) == 1:
            all1.append(movieNumbers[0].text)
        else:
            all1.append("Unknown")
        movieCast = movie.find("p", class_="")
        try:
            casts = movieCast.text.replace("\n", "").split('|')
            casts = [x.strip() for x in casts]
            casts = [casts[i].replace(j, "") for i, j in enumerate(["Director:", "Stars:"])]
            movieDirector.append(casts[0])
            movieStars.append([x.strip() for x in casts[1].split(",")])
        except:
            casts = movieCast.text.replace("\n", "").strip()
            movieDirector.append("Unknown")
            movieStars.append([x.strip() for x in casts.split(",")])

        flatten_directors = list(chain.from_iterable(movieDirector))
        flatten_stars = list(chain.from_iterable(movieStars))
        directors = listToString(flatten_directors)
        stars = listToString(flatten_stars)
        all1.append(directors)
        all1.append(stars)
        if movie.find("span", class_="metascore unfavorable") is not None:
            all1.append(movie.find("span", class_="metascore unfavorable").text.rstrip())
        else:
            all1.append("Unknown")
        all1.append(movie.find("span", class_="genre").text.rstrip().replace("\n", "").split(","))
        if movie.find("span", class_="runtime") is not None:
            all1.append(movie.find("span", class_="runtime").text[:-4])
        else:
            all1.append("Unknown")
        all.append(all1)
    return all


results = []
no_pages = 20
for k in range(1, no_pages + 1):
    results.append(get_data(k))
flatten = lambda l: [item for sublist in l for item in sublist]
df = pd.DataFrame(flatten(results),
                  columns=['Title', 'Rating', 'Description', 'Votes', 'Directors', 'Stars', 'Meta Score', 'Genre',
                           'Duration'])

print(df)
