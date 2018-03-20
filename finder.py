"""
    Author: Marek Tamaskovic
    email: tamaskovic.marek -[at]- gmail.com
"""

import re
import const
import requests


from person import *


def get(block, room):
    "Post request to kn.vutbr.cz and retrieve names with correct parameters"
    names = list()

    r = requests.get(
        'http://kn.vutbr.cz/search/index.html?str='+str(block)+'-'+str(room))

    if r.status_code is not 200:
        print("ERROR: site status code: ", r.status_code)
        return None

    if "Data nenalezena" in r.text:
        return None

    regex = re.compile("<\/font>\s(.*)\s(.*)<\/th>")
    matches = re.finditer(regex, r.text)

    for match in matches:
        p_name = str(match.group(1))
        p_surname = str(match.group(2))

        if p_surname.endswith(('á', 'Á')):
            p_gender = const.FEMALE
        else:
            p_gender = const.MALE

        names.append(Person(p_name, p_surname, p_gender))
    return names
