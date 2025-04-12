import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

Titles_Name = []
Prices = []
Reviews = []
Titles_Links = []
Images_Links = []

for page in range(1, 51):
    url = f'https://www.amazon.com/s?k=laptop&page={page}'
    r = requests.get(url, headers=headers)

    print(f"Page {page} status: {r.status_code}")
    if r.status_code != 200:
        print("Request failed or got blocked")
        continue

    soup = BeautifulSoup(r.content, 'html.parser')

    titles = soup.find_all('h2', class_='a-size-medium a-spacing-none a-color-base a-text-normal')
    prices = soup.find_all('span', class_='a-price-whole')
    reviews = soup.find_all('i', class_='a-icon a-icon-star-small a-star-small-4-5')
    links = soup.find_all('a', class_='a-link-normal s-line-clamp-2 s-link-style a-text-normal')
    img_tags = soup.find_all('img', class_='s-image') 

    for title in titles:
        Titles_Name.append(title.getText(strip=True))

    for price in prices:
        Prices.append(price.getText(strip=True))

    for review in reviews:
        span = review.find('span')
        Reviews.append(span.getText(strip=True) if span else "N/A")

    for link in links:
        href = link.get('href')
        if href:
            Titles_Links.append("https://www.amazon.com" + href)

    for img in img_tags:
        src = img.get('src')
        if src:
            Images_Links.append(src)

    time.sleep(2)

min_len = min(len(Titles_Name), len(Prices), len(Reviews), len(Titles_Links), len(Images_Links))

df = pd.DataFrame({
    "Titles": Titles_Name[:min_len],
    "Prices": Prices[:min_len],
    "Reviews": Reviews[:min_len],
    "Title Links": Titles_Links[:min_len],
    "Image Links": Images_Links[:min_len]
})

df.to_csv('C:\\Users\\HM Laptops\\Desktop\\Web Scrapping\\Amazon_Laptops_Multi_pages.csv', index=False)
print("CSV saved successfully!")
