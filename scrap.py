# pip install requests
# pip install html5lib
# pip install bs4

import requests
import json
import csv
import re
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
}

# Part 1
def get_data(main_url, n):
    data = {}
    k = 0
    for j in range(1,n):
        url = main_url + "&page=" + str(j)
        if j == 1:
            url =main_url
        base_url = "https://www.amazon.in"
        r = requests.get(url, headers=headers)
        html_content = r.content
        soup = BeautifulSoup(html_content, 'html.parser')

        s_urls = soup.find_all('a', class_="a-text-normal")
        s_names = soup.find_all("span", class_="a-size-medium a-color-base a-text-normal")
        s_prices = soup.find_all("span", class_="a-offscreen")
        s_ratings = soup.find_all("span", class_="a-icon-alt")
        s_reviews = soup.find_all("span", class_="a-size-base s-underline-text")
        i=0
        for names in s_names:
            if i < len(s_ratings):
                rating = s_ratings[i].text.split(" ")[0]
            else:
                rating = ""
            if i < len(s_reviews):
                reviews = s_reviews[i].text
            else:
                reviews = ""
            if i < len(s_prices):
                price = s_prices[i].text
            else:
                price = ""
            data[k+i] = {
                "url" : base_url + s_urls[i].get('href'),
                "name" : names.text,
                "price" : price,
                "rating" : rating,
                "review" : reviews
            }
            i+=1
        k+=i
    return data

base_url = "https://www.amazon.in/"
url = base_url+"s?k=bags"
final_data = get_data(url, 21)


# Part 2
p_datas = {}
a=0
for key in final_data:
    if a<200:
        url = final_data[key]["url"]
        r = requests.get(url, headers=headers)
        html_content = r.content
        soup = BeautifulSoup(html_content, 'html.parser')

        if soup.find_all("ul", class_="a-unordered-list a-vertical a-spacing-mini"):
            s_decription = soup.find_all("ul", class_="a-unordered-list a-vertical a-spacing-mini")[0].text
        else:
            s_decription = "Null"

        # s_asin = url.split("/")[4]
        if soup.find("th", text= re.compile("ASIN")):
            s_asin = soup.find("th", text=re.compile("ASIN")).find_next('td').contents[0]
        elif soup.find("span", text= re.compile("ASIN")):
            s_asin = soup.find("span", text= re.compile("ASIN")).find_next('span').contents[0]
        else:
            s_asin = "Null"

        if soup.find_all("ul", class_="a-unordered-list a-vertical a-spacing-mini"):
            s_p_decription = soup.find_all("ul", class_="a-unordered-list a-vertical a-spacing-mini")[0].text
        else:
            s_p_decription = "Null"

        if soup.find("th", text=re.compile("Manufacturer")):
            s_manufacturer = soup.find("th", text=re.compile("Manufacturer")).find_next('td').contents[0]
        elif soup.find_all("span", text=re.compile("Manufacturer")):
            span = soup.find_all("span", text=re.compile("Manufacturer"))[len(soup.find_all("span", text=re.compile("Manufacturer")))-1]
            s_manufacturer = span.find_next('span').contents[0]
        else:
            s_manufacturer = "Null"

        p_datas[key] = {
            "decription":s_decription,
            "asin":s_asin,
            "product_decription":s_p_decription,
            "manufacturer":s_manufacturer
        }
        a+=1
    else:
        break


# Part 1 File
data_file = open('products.csv', 'w', encoding="utf-8")
csv_writer = csv.writer(data_file)
count = 0
for key in final_data:
    if count ==0:
        header = final_data[key].keys()
        csv_writer.writerow(header)
        count+=1
    csv_writer.writerow(final_data[key].values())
data_file.close()

# Part 2 File
data_file = open('product_details.csv', 'w', encoding="utf-8")
csv_writer = csv.writer(data_file)
count = 0
for key in p_datas:
    if count ==0:
        header = p_datas[key].keys()
        csv_writer.writerow(header)
        count+=1
    csv_writer.writerow(p_datas[key].values())
data_file.close()
