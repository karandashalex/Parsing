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
    return flats


def main():
    print('Start parsing. Wait...')

    # Get html
    html = get_html(REALT_URL)

    # Get number of last page
    #page_count = get_page_count(html)
    page_count = 1
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
