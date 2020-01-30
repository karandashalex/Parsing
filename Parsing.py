import urllib.request
from bs4 import BeautifulSoup

# Main URL of website realt.by
REALT_URL = 'https://realt.by/sale/flats/?view=0'


# Open url and return html
def get_html(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req).read()


# Get html and return last page number
def get_page_count(html):
    soup = BeautifulSoup(html, features='html.parser')
    pages = soup.find('div', class_='uni-paging')
    last_page = pages.find_all('a')[-1].text
    return int(last_page)


# Get html and parse one page. Return flats list
def parse(html):
    # Get center table with flats
    soup = BeautifulSoup(html, features='html.parser')
    table = soup.find('div', class_='bd-table')

    # Find in page all flats and append all of them in list
    header = table.find_all('div', class_='bd-table-item-header')
    flats = []
    for head in header:
        pl = head.find_all('div', class_='pl')
        address = head.find('div', class_='ad').a.text.split(',')
        floors = head.find('div', class_='ee').span.text.split('/')
        max_floor = floors[1].strip().split(' ')[0]
        try:
            house_type = floors[1].strip().split(' ')[1]
        except:
            house_type = ''

        sity = ''
        street = ''
        house = ''
        total_price = ''
        price = ''
        if len(address):
            sity = address.pop(0).strip()
        if len(address):
            street = address.pop(0).strip()
        if len(address):
            house = address.pop(0).strip()
        prlist = [''.join(pr.text.split()) for pr in head.find('div', class_='cena').find_all('span')]
        for pr in prlist:
            if pr.find('руб/кв') > 0:
                price = pr[:pr.find('руб/кв')]
                if price.find('млн') > 0:
                    price = int(float(price[:price.find('млн')].replace(',', '.')) * 1000000)
            elif pr.find('руб'):
                total_price = pr[:pr.find('руб')]
                if total_price.find('млн') > 0:
                    total_price = int(float(total_price[:total_price.find('млн')].replace(',', '.')) * 1000000)

        flats.append({
            'rooms': head.find('div', class_='kv').span.text.strip().split('/')[0],
            'separate_rooms': head.find('div', class_='kv').span.text.strip().split('/')[1],
            'area': head.find('div', class_='ra').span.text.strip(),
            'sity': sity,
            'street': street,
            'house': house,
            'floor': floors[0].strip(),
            'max_floor': max_floor,
            'house_type': house_type,
            'total_square': pl[0].span.text.strip().split('/')[0],
            'live_square': pl[0].span.text.strip().split('/')[1],
            'kitchen_square': pl[0].span.text.strip().split('/')[2],
            'year': pl[1].span.text.strip(),
            'balcony': pl[2].span.text.strip(),
            'total_price': total_price,
            'price': price
        })
    return flats


def main():
    print('Start parsing. Wait...')

    # Get html
    html = get_html(REALT_URL)

    # Get number of last page
    page_count = get_page_count(html)
    #page_count = 1
    print('Find %d pages' % page_count)

    # List with all flats
    allflats = []

    # Find flats on all pages
    for page in range(0, page_count):
        print('Parsing %d%%' % (page / page_count * 100))
        html = get_html(REALT_URL + '&page=%d' % page)
        allflats.extend(parse(html))

    print('Parsing finished')

    # Print list
    for flat in allflats:
        print(flat)


if __name__ == '__main__':
    main()
