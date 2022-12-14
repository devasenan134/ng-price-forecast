from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests

'''
https://news.google.com/search?q=natural%20gas&hl=en-IN&gl=IN&ceid=IN%3Aen

https://news.google.com/search?q=natural%20gas%20when%3A1d&hl=en-IN&gl=IN&ceid=IN%3Aen
'''


root = "https://news.google.com"
link = "https://news.google.com/search?q=natural%20gas%20when%3A1d&hl=en-IN&gl=IN&ceid=IN%3Aen"

req = Request(link, headers={"User-Agent": "Mozilla/5.0"})
webpage = urlopen(req).read()

# print(webpage)
# class="NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc"

news24 = []

with requests.Session() as c:
    soup = BeautifulSoup(webpage, 'html.parser')
    # print(soup)
    for item in soup.find_all('div', attrs={'class': 'NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc'}):
        link = (root + "/" + item.find('a', href=True)["href"] + "\n").split("&sa=U&")[0]
        title = item.find("a", attrs={'class': 'DY5T1d RZIKme'}).get_text()
        source = item.find("a", attrs={'class': 'wEwyrc AVN2gc uQIVzc Sksgp'}).get_text()
        time = item.find("time", attrs={'class': 'WW6dff uQIVzc Sksgp'}).get_text()

        img = item.find("img", attrs={'class': 'tvs3Id QwxBBf'})['srcset']

        news24.append([title, source, time, link, img])
        
print(news24)
