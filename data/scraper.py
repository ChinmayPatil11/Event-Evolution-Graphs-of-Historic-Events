import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def create_dataframe(link):
    page = requests.get(link).text
    soup = BeautifulSoup(page, 'lxml')
    tags = soup.findAll('li')
    events = []
    for tag in tags:
        event = tag.text
        events.append(event)
    final_events = []
    for e in events:
        es = re.search(r"\d{4}: .+", e)
        if es != None:
            final_events.append(es.string)
    year_list = []
    event_list = []
    for event in final_events:
        year, eve = event.split(' ', 1)
        year_list.append(year)
        event_list.append(eve)
    df = pd.DataFrame({'Year': year_list, 'Events': event_list})
    return df

