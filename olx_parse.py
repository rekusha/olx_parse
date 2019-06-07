import requests
from bs4 import BeautifulSoup
import mysql.connector

def work_bd_insert(data):
    con = mysql.connector.connect(user='python_test',
    password='1234567890', host='192.168.0.3',
    port='3307', database='python_test', )
    c = con.cursor()
    for zzz in data:
        if zzz in work_bd_select():
            pass
            #print('dublicate')
        else:
            c.execute('INSERT INTO all_url_parse(url) VALUES (\'%s\')'%zzz)
            #print('new')
    con.commit()
    con.close()
    print('insert Ok')

def work_bd_select():
    con = mysql.connector.connect(user='python_test',
    password='1234567890', host='192.168.0.3',
    port='3307', database='python_test', )
    c = con.cursor()
    inbase_list = []
    c.execute('SELECT * FROM all_url_parse')
    for a,b in c:
        inbase_list.append(b)
    con.close()
    return inbase_list

#return url of starting page in html format
def get_html(url):
    r = requests.get(url)
    return r.text

#get number of pages from html data
def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_ ='pager rel clr').find_all(
                    'a', class_ = 'block br3 brc8 large tdnone lheight24'
                    )[-1].get('href')
    total_pages = pages.split('=')[-1]
    return int(total_pages)

#from all pages take all urls of announcement and return they in [list]
def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('table', class_='fixed offers breakword redesigned').find_all(
                    'a', class_='marginright5 link linkWithHash detailsLink')
    ads_list = []
    for ad in ads:
        ads_list.append(ad.get('href').split('#')[0])
    return ads_list

def main():
    url ='https://www.olx.ua/nedvizhimost/kvartiry-komnaty/prodazha-kvartir-komnat/kiev/?search%5Bprivate_business%5D=private&search%5Border%5D=filter_float_price%3Aasc&'
    base_url = 'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/prodazha-kvartir-komnat/kiev/?search%5Bprivate_business%5D=private&search%5Border%5D=filter_float_price%3Aasc&'
    page_part = 'page='
    total_pages = get_total_pages(get_html(url))
    print('pages %s' % total_pages)
    all_link_list = []
    for i in range(1, 2):# total_pages+1):
        url_gen = base_url + page_part + str(i)
        html = get_html(url_gen)
        all_link_list.extend(get_page_data(html))
    work_bd_insert(all_link_list)
    print(len(work_bd_select()))

if __name__ == '__main__':
    main()
