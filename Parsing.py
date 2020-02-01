import urllib.request
from bs4 import BeautifulSoup
import csv

# Main URL of website realt.by
REALT_URL = 'https://realt.by/sale/flats/?view=0'
# String with parameters for parsing
param_str = 'sity=Копище'#, rooms>=1, floor>=2, total_price<1040000, floor<15'
# All parameters used
params = ['rooms', 'separate_rooms', 'area', 'sity', 'street', 'house', 'floor', 'max_floor', 'house_type',
          'total_square', 'live_square', 'kitchen_square', 'year', 'repare_year', 'balcony', 'total_price', 'price']
# All signs used
signs = ['>=', '<=', '!=', '=', '>', '<']

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
def parse_page(html):
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
        year = pl[1].span.text.strip().split(' ')[0]
        try:
            repare_year = pl[1].span.text.strip().split(' ')[1]
        except:
            repare_year = ''
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
            'year': year,
            'repare_year': repare_year,
            'balcony': pl[2].span.text.strip(),
            'total_price': total_price,
            'price': price
        })
    return flats


def parse(page=0):
    print('Start parsing. Wait...')
    # Get html
    html = get_html(REALT_URL)
    if page == 0:
        # Get number of last page
        page_count = get_page_count(html)
    else:
        page_count = page
    print('Find %d pages' % page_count)
    # List with all flats
    allflats = []
    # Find flats on all pages
    for page in range(0, page_count):
        print('Parsing %d%%' % (page / page_count * 100))
        html = get_html(REALT_URL + '&page=%d' % page)
        allflats.extend(parse_page(html))
    print('Parsing %d records finished' % len(allflats))
    return allflats


# Write all flats in csv-file as dictionary. Russian Windows used delimiter=';' and  lineterminator='\n'
def write_csv(flats, filename):
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=list(flats[0].keys()), quoting=csv.QUOTE_NONNUMERIC,
                                lineterminator='\n',
                                delimiter=';')
        writer.writeheader()
        for flat in flats:
            writer.writerow(flat)


# Read all data from csv-file and return list of dictionaries
def read_csv(filename):
    flats_list = []
    with open(filename) as f:
        reader = csv.DictReader(f, lineterminator='\n', delimiter=';')
        for row in reader:
            d = {}
            d.update(row)
            flats_list.append(d)
    return (flats_list)


# Function create parameters list from string with parameters if string is good. And function create parameters list
# with error items if string is bad. Еhe first return value is True or False, and second is the list.
# Which element is list and contains parameter name, parameter sign and value.
def create_param_list(pr_str, pr, sgn):
    # Parameters list
    pr_str_list = pr_str.strip().split(',')
    # List with good parameters
    pr_list = []
    # List with bad parameters
    err_pr_list = []
    # The analysis of the sign
    for p in pr_str_list:
        for s in sgn:
            if p.find(s) >= 0:
                pr_list.append([p.split(s)[0].strip(), s, p.split(s)[1].strip()])
                break
        else:
            err_pr_list.append(p.strip())
    # The analysis of parameters
    param_set = set()
    for z in pr_list:
        param_set.add(z[0])
    s = param_set - set(pr)
    if len(s):
        err_pr_list.append(', '.join(s))
    # Finish analysis
    if len(err_pr_list) > 0:
        return False, err_pr_list
    else:
        return True, pr_list


# Compare two volumes used sign
def compare(vol1, sign, vol2):
    if sign == '>=':
        return vol1 >= vol2
    elif sign == '<=':
        return vol1 <= vol2
    elif sign == '!=':
        return vol1 != vol2
    elif sign == '=':
        return vol1 == vol2
    elif sign == '>':
        return vol1 > vol2
    elif sign == '<':
        return vol1 < vol2


def main():
    # allflats = parse(1)

    # Print list
    # for flat in allflats:
    #     print(flat)

    # Write data in csv-file
    # write_csv(allflats, 'Realt.csv')

    # Read data from csv-file
    fl = read_csv('Realt.csv')

    # Print list
    # for flat in fl:
    #     print(flat)

    a, param_str_list = create_param_list(param_str, params, signs)
    if not a:
        print('Error param(s): ' + ', '.join(param_str_list))
        return

    for flat in fl:
        for pr in param_str_list:
            if not compare(flat[pr[0]], pr[1], pr[2]):
                break
        else:
            print(flat)


if __name__ == '__main__':
    main()
