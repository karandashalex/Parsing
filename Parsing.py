import urllib.request
from bs4 import BeautifulSoup


def get_html(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req).read()


def parse(html):
    soup = BeautifulSoup(html, features='html.parser')
    table = soup.find('div', class_='bd-table')
    header = table.find_all('div', class_='bd-table-item-header')
    flats = []
    for head in header:
        pl = head.find_all('div', class_='pl')
        flats.append({
            'c': head.find('div', class_='kv').span.text.strip(),
            'area': head.find('div', class_='ra').span.text.strip(),
            'address': head.find('div', class_='ad').a.text.strip(),
            'floor': head.find('div', class_='ee').span.text.strip(),
            'square': pl[0].span.text.strip(),
            'year': pl[1].span.text.strip(),
            'balcony': pl[2].span.text.strip(),
            'price': [''.join(pr.text.split()) for pr in head.find('div', class_='cena').find_all('span')]
            # 'price': [pr.text.strip().split() for pr in head.find('div', class_='cena').find_all('span')]
        })
    for flat in flats:
        print(flat)


def main():
    print('start')
    html = get_html('https://realt.by/sale/flats/?view=0&page=0')
    parse(html)
    print('good work')


if __name__ == '__main__':
    main()
