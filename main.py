import csv
import requests
from bs4 import BeautifulSoup

# get the URL from the page we're scraping
url = "https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm&sort=user_rating%2Cdesc"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

# send a get request to the URL
urlResponse = requests.get(url, headers=headers)

# test if the request succeeded (status 200)
if urlResponse.status_code == 200:
    # create an object with the HTML parsing from the URL
    soup = BeautifulSoup(urlResponse.text, "html.parser")

    # get the elements with the h3 tag in the soup object
    headlines = soup.find_all("div", class_= "sc-b85248f1-0 bCmTgE cli-children")

    # create a CSV archive
    file = open('scrappedData.csv', 'w', newline = '', encoding = 'utf-8')
    writer = csv.writer(file)
    headers = ['Nome do Filme', 'Nota']
    writer.writerow(headers)

    # iterate through the elements and write the headlines
    for headline in headlines:
        # extract the movie headline
        title = headline.find("h3", class_= "ipc-title__text").text.strip()
        rating = headline.find("span", class_="ipc-rating-star").text.strip()

        # get rid of the unusefull text on rating
        parts = rating.split("\u00A0")
        rating = parts[0]

        # write on the CSV file
        row = [title, rating]
        writer.writerow(row)

    file.close()  # Close the file outside the loop

    print("Dados exportados para scrappedData.csv.")

else:
    print("Falha ao acessar a página:", urlResponse.status_code)
