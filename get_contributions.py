import requests
import json
import urllib2
from bs4 import BeautifulSoup

def get_public_contributions(users):
    public_contributions = []
    for user in users:
        public_contributions.append(parse_url(user))
    print public_contributions

def parse_url(user):
    public_contributions = 0
    url = 'https://github.com/' + user
    usock = urllib2.urlopen(url)
    soup = BeautifulSoup(usock.read())
    x = soup.find_all('span','num')
    x = x[0]
    for items in x:
        numbers = items.split();
        public_contributions = numbers[0]
    print public_contributions
    return public_contributions

get_public_contributions(['v', 'k', 'sagnew', 'yesdnil5'])
