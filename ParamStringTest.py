# String with parameters for parsing
param_str = 'sity=Минск, price<400000, price>200000, rooms>=2, floor!=1'
# All parameters used
params = ['rooms', 'separate_rooms', 'area', 'sity', 'street', 'house', 'floor', 'max_floor', 'house_type',
          'total_square', 'live_square', 'kitchen_square', 'year', 'repare_year', 'balcony', 'total_price', 'price']
# All signs used
signs = ['>=', '<=', '!=', '=', '>', '<']


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


a, param_str_list = create_param_list(param_str, params, signs)
if a:
    print(param_str_list)
else:
    print('Error param(s): ' + ', '.join(param_str_list))
