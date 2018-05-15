from bs4 import BeautifulSoup
import urllib.request
import time
import json

def Take_subpage(url):
    header = {'user-agent': 'Mozilla/5.0 (Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
    r = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(r, "lxml")
    result = []
    name = soup.find("h1", {"class":"c-product-detail__name qa-pd-name"}).text
    result.append(name)
    price = soup.find("meta", {"name":"product:price:amount"})["content"]
    result.append(price)
    merkraw = soup.find("dd", {"class":"c-deflist__value qa-pd-attribute-value"}).text
    merk = merkraw.replace("\n", "")
    result.append(merk)
    return result

def Take_allpage(url):
    data = {}
    data['Kamera'] = []
    n = 1
    while n < 101:
        if (n < 2):
            parentpage = urllib.request.urlopen(url).read()
        else:
            parentpage = urllib.request.urlopen(url+'?page='+str(n)).read()
        pagesoup = BeautifulSoup(parentpage, "lxml")
        alllink = pagesoup.findAll("a", {'class':'product__name line-clamp--2 js-tracker-product-link'})
        try:
            for product in alllink:
                try:
                    oneproduct = Take_subpage('https://www.bukalapak.com'+product['href'])
                    print(oneproduct)
                    data['Kamera'].append({
                        'Nama': oneproduct[0],
                        'Harga': oneproduct[1],
                        'Merek': oneproduct[2]
                    })
                except:
                    pass
                time.sleep(3)
        except KeyboardInterrupt:
            break
        n=n+1
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
    return 0

Take_allpage("https://www.bukalapak.com/c/kamera/kamera-analog")
