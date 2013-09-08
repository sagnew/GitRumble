import requests
import json
import urllib2
from bs4 import BeautifulSoup

def build_user_dict(users):
    user_dict = {}
    for user in users:
        user_dict[user] = get_public_contributions(user)
    return user_dict

def get_public_contributions(user):
    public_contributions = 0
    url = 'https://github.com/' + user
    usock = urllib2.urlopen(url)
    soup = BeautifulSoup(usock.read())
    x = soup.find_all('span','num')
    x = x[0]
    for items in x:
        numbers = items.split();
        public_contributions = numbers[0]
    return public_contributions
