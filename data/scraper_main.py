import pandas as pd
from scraper import create_dataframe

url_start = 'https://en.wikipedia.org/wiki/Timeline_of_the_'
url_end = '_century'
urls = ['17th','18th','19th','20th']
for i in urls:
    url = url_start + i + url_end
    df = create_dataframe(url)
    filename = i + '_century.csv'
    df.to_csv(filename,index=False)
