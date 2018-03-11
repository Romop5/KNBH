#!/usr/bin/env python3.6

"""
    Author: Marek Tamaskovic
    email: tamaskovic.marek -[at]- gmail.com
"""

import requests
from bs4 import BeautifulSoup
import re
import const


class Person():
    name = ""
    surname = ""
    gender = None

    def getName(self):
        return self.name + " " + self.surname

    def isWoman(self):
        return self.gender is const.FEMALE


def get(block, room):
    "Post request to kn.vutbr.cz and retrieve names with correct parameters"
    names = list()

    r = requests.get('http://kn.vutbr.cz/search/index.html?str='+str(block)+'-'+str(room))

    if r.status_code is not 200:
        print("ERROR: site status code: ", r.status_code)
        return None

    if "Data nenalezena" in r.text:
        return None

    parsed_html = BeautifulSoup(r.text, 'html.parser')

    counter = 0

    p = re.compile("<td.*>.*>((Jméno)|(Blok)|(Příjmení)):(.*>){3}.*<\/td>")

    for i in parsed_html.td:
        counter += 1
        if counter == 6:
            for line in i:
                string = str(line)
                person = Person()
                for m in p.finditer(string):
                    asd = str(m.group())
                    if "Jméno" in asd:
                        person.name = asd[40:-5]
                    elif "jmen" in asd:
                        person.surname = asd[43:-5]
                        if person.surname.endswith(('á','Á')):
                            person.gender = const.FEMALE
                        else:
                            person.gender = const.MALE
                        names.append(person)
                        person = Person()

    return names
