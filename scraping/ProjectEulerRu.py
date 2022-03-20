import csv
from bs4 import BeautifulSoup
import requests
import time


anlist = []

with open ("data.csv", "w", encoding='cp1251') as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(["Номер задачи", "Ссылка на задачу", "Cсылка на оригинал""Название зачачи"])
print("All's OK")

def get_data(url):
    global anlist
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    }

    r = requests.get(url=url, headers=headers)
    # with open("index.html", "w") as file:
    #     file.write(r.text)
    soup = BeautifulSoup(r.text, "lxml")
    pagination = soup.find_all("a")
    pagination_number = len(pagination) - 74
    
    for j in range (1, pagination_number+1):
        src = requests.get(f"https://euler.jakumo.org/problems/pg/{j}.html", headers=headers)
        soup = BeautifulSoup(src.text, "lxml")
        names = soup.find_all("td")

        names = names[2 :]
        for i in names:
            print (i.text)
            try: int(i.text)
            except (ValueError, UnicodeError, UnicodeEncodeError):
                anlist.append(i.text)
                with open ("data.csv", "a", encoding="utf-8") as file:
                    writer = csv.writer(file, delimiter=";")
                    writer.writerow(anlist)
                anlist = []

            else:
                
                anlist.append(i.text)
                anlist.append(f"https://euler.jakumo.org/problems/view/{i.text}.html")
                anlist.append(get_original(i.text))
                #print (f"https://euler.jakumo.org/problems/view/{i.text}.html")
        print (f"Parced {j}/{pagination_number}")
        time.sleep(2)


def get_original(number):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    }

    r = requests.get(url=f"https://euler.jakumo.org/problems/view/{number}.html", headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    try: soup.find(target="_blank").get('href')
    except AttributeError:
        original_url = "Нет адресса"
    else:
        original_url = soup.find(target="_blank").get('href')
    return original_url

            

get_data("https://euler.jakumo.org/problems/pg/1.html")

print("FINISH")



