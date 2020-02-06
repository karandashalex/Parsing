import urllib.request
from bs4 import BeautifulSoup
import csv

# Main URL of website realt.by
REALT_URL = 'https://realt.by/sale/flats/?view=0'
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
    # Get object of BeautifulSoup
    soup = BeautifulSoup(html, features='html.parser')
    pages = soup.find('div', class_='uni-paging')
    last_page = pages.find_all('a')[-1].text
    return int(last_page)


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
    return flats_list


# Function create parameters list from string with parameters if string is good. And function create parameters list
# with error items if string is bad. The first return value is True or False, and second is the list.
# Which element is list and contains parameter name, parameter sign and value.
def create_param_list(pr_str, pr, sgn):
    # Parameters list
    try:
        pr_str_list = pr_str.strip().split(',')
    except AttributeError:
        return True, []
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


# Compare two string used sign. If sign is '=' use find method
def compare_str(vol1, sign, vol2):
    vol1 = str(vol1).lower()
    vol2 = str(vol2).lower()

    if sign == '>=':
        return vol1 >= vol2
    elif sign == '<=':
        return vol1 <= vol2
    elif sign == '!=':
        return vol1 != vol2
    elif sign == '=':
        return vol1.find(vol2) >= 0
    elif sign == '>':
        return vol1 > vol2
    elif sign == '<':
        return vol1 < vol2


# Compare two volumes used sign
def compare_digit(vol1, sign, vol2):
    if not vol1.lstrip('-').replace('.', '', 1).isdigit():
        vol1 = 0.0
    else:
        vol1 = float(vol1)

    if not vol2.lstrip('-').replace('.', '', 1).isdigit():
        vol2 = 0.0
    else:
        vol2 = float(vol2)

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


# Get html and parse one page. Return flats list
def parse_page(html, param_str_list):
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
        record = {
            'rooms': head.find('div', class_='kv').span.text.strip().split('/')[0],
            'separate_rooms': head.find('div', class_='kv').span.text.strip().split('/')[1],
            'area': head.find('div', class_='ra').span.text.strip(),
            'sity': sity,
            'street': street,
            'house': house,
            'floor': floors[0].strip(),
            'max_floor': max_floor,
            'house_type': house_type,
            'total_square': pl[0].span.text.strip().split('/')[0].replace(',', '.'),
            'live_square': pl[0].span.text.strip().split('/')[1].replace(',', '.'),
            'kitchen_square': pl[0].span.text.strip().split('/')[2].replace(',', '.'),
            'year': year,
            'repare_year': repare_year,
            'balcony': pl[2].span.text.strip(),
            'total_price': total_price,
            'price': price
        }
        for pr in param_str_list:
            if pr[0] in ['total_square', 'live_square', 'kitchen_square', 'total_price', 'price']:
                if not compare_digit(record[pr[0]], pr[1], pr[2]):
                    break
            else:
                if not compare_str(record[pr[0]], pr[1], pr[2]):
                    break
        else:
            flats.append(record)
    return flats


# Get count of parsing pages. If it get 0 or nothing, function parse all pages. It returns flats list as result
def parse(param_str=[]):
    # Checking the string with parameters
    a, param_str_list = create_param_list(param_str, params, signs)
    if not a:
        print('Error param(s): ' + ', '.join(param_str_list))
        print('Enter the correct parameters. Program stopped.')
        return
    print('Url search. Wait...')

    # Get html
    try:
        html = get_html(REALT_URL)
    except urllib.error.URLError:
        print('URL Error. Program stopped')
        return
    except Exception as e:
        print(f'Program stopped. Error getting HTML : {e}')
        return

    # Get number of last page
    # For example parse one page.
    page = 3
    try:
        if page == 0:
            # Get number of last page
            page_count = get_page_count(html)
        else:
            page_count = page
        print('Find %d pages' % page_count)
    except (AttributeError, IndexError):
        print('Error accessing page content. Program stopped')
        return
    except Exception as e:
        print(f'Program stopped. Error getting HTML : {e}')
        return

    # List with all correct flats
    all_flats = []
    # Find flats on all pages
    for page in range(page_count):
        print('Parsing %3.2f%%' % (page / page_count * 100))
        html = get_html(REALT_URL + '&page=%d' % page)
        all_flats.extend(parse_page(html, param_str_list))
    print('Parsing %d records finished' % len(all_flats))
    return all_flats


# Find all records in 'fl' list used param_str
def find_in_list(fl, param_str):
    find_list = []
    for flat in fl:
        for pr in param_str:
            if pr[0] in ['total_square', 'live_square', 'kitchen_square', 'total_price', 'price']:
                if not compare_digit(flat[pr[0]], pr[1], pr[2]):
                    break
            else:
                if not compare_str(flat[pr[0]], pr[1], pr[2]):
                    break
        else:
            find_list.append(flat)
    return find_list


def main():
    # String with parameters for parsing
    param_string = 'kitchen_square>=8, kitchen_square<=11.7, sity=коп, year>2018'
    # param_string = 'price>4000'
    # param_string = 'rooms>1, rooms<=3, year>2015'
    # param_string = 'rooms>1, rooms<=3, kitchen_square>=4.7, kitchen_square<=11.7, year>2000, house_type!=п'

    # Parse
    all_flats = parse(param_string)

    # Write data in csv-file
    # write_csv(all_flats, 'Realt.csv')

    # Read data from csv-file
    #all_flats = read_csv('Realt.csv')

    # Print list
    for f in all_flats:
        print(f)

if __name__ == '__main__':
    main()
