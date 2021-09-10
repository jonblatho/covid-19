import json
from . import geo
from . import date
from . import data, calc

geo = geo
date = date
data = data
calc = calc

# Outputs JSON for the given dictionary or list to the given path.
def save_json(x, path, quiet=False):
    with open(path, 'w+') as output_file:
        output_file.write(json.dumps(x, separators=(',', ':')))
        if not quiet:
            print(f'Saved {path}')

# Returns only the unique elements in a list
def unique(l):
    unique_list = []
    for item in l:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list