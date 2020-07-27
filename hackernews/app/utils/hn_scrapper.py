import datetime
import re

import requests
from bs4 import BeautifulSoup as bs


class GrabberError(Exception):
    pass


URL = 'https://news.ycombinator.com/'
RE_TIME = r'(?P<timedelta>\d+)\s*(?P<time_format>week|day|hour|minute|second)(?:s)?\s+ago'


def get_news_list():
    try:
        res = requests.get(URL)
        data_dict_list = list()
        timedeltaFilterer = re.compile(RE_TIME, flags=re.I)
        soup = bs(res.text, 'html.parser')
        itemsTable = soup.find(name='table', class_='itemlist')

        subjectRows = itemsTable.find_all(name='tr', class_='athing')

        for subjectRow in subjectRows:
            data_dict = dict()

            # Get news url and subject from first <tr>
            anchor = subjectRow.find(name='a', class_='storylink')
            data_dict['id'] = subjectRow.attrs.get('id')
            data_dict['url'] = anchor.attrs.get('href')
            data_dict['title'] = anchor.text.strip()
            # Get post age from the immediate next <tr>
            additionalInfoRow = subjectRow.next_sibling  # Getting next <tr>
            # Getting <td> having actual information
            subtextCol = additionalInfoRow.find(name="td", class_='subtext')

            timedeltaStr = subtextCol.find(
                name='span', class_='age').text.strip()
            age, ageFormat = timedeltaFilterer.search(
                timedeltaStr).group('timedelta', 'time_format')
            data_dict['post_age'] = datetime.timedelta(**{ageFormat + 's': int(age)})
            data_dict['approx_created_at'] = datetime.datetime.now() - \
                data_dict['post_age']

            data_dict_list.append(data_dict)

        return data_dict_list
    except Exception:
        raise GrabberError


if __name__ == '__main__':
    print(get_news_list())
