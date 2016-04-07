# -*- coding: utf8 -*-
import twitter
from datetime import datetime
import requests
import re
import json


def get_magnet_link(url):
    response = requests.get(url)
    source_string = response.content
    pattern = re.compile(r'(?<=id="a_magnet" href=")(.*?)">')
    result = pattern.search(source_string)
    if result:
        return result.group(1)
    else:
        return 'no result'


def load_config(config_path='config.json'):
    with open(config_path) as fd:
        conf = json.load(fd)
        return conf


def save_config(config_path='config.json', data=None):
    with open(config_path, 'w') as fd:
        json.dump(data, fd)


def load_ani_list(config_path='ani_list.txt'):
    ani_patterns = []
    with open(config_path) as fd:
        ani_patterns = [_s for _s in fd]
    return ani_patterns


def main_flow():
    conf = load_config()
    api = twitter.Api(consumer_key='xBRI3AyW9KISPblLLJmdzpyKe',
                      consumer_secret='knpZVkRTCnRKf83rZm2H5E26VRjTzQWhI4NXF6eKbIWdJ5ZEEf',
                      access_token_key='14957307-Z3bxikJTeorKvWqPpmKpWLjTOHGZ9fkL0zmje0dwc',
                      access_token_secret='M1doOrG0hxmQzWAV0BPr7e9cWu2kiZ5dNGIhd8qpchaSX')

    patterns = load_ani_list()
    statuses = api.GetUserTimeline(
        screen_name='dmhyrss',
        since_id=conf['since_id'],
        max_id=conf['max_id'],
        count=conf['count'])
    if(len(statuses) != 0):
        conf['since_id'] = statuses[0].id

    result = []
    magnet_link_list = []
    for s in statuses:
        text = s.text.encode('utf8')
        # conf['max_id'] = s.id
        # print(text)
        # print(s.id)
        result.append(text)
        result.append(s.created_at)
        result.append('')
        for pattern in patterns:
            if text.startswith(pattern.replace('\n', '').strip()):
                magnet_link_list.append(text)
                if s.urls:
                    magnet_link_list.append(
                            get_magnet_link(s.urls[0].expanded_url))
                magnet_link_list.append('')
    save_config(data=conf)

    # save result and save magnet link
    result_name = datetime.now().strftime("%Y%m%d%H%M%S") + '.txt'
    magnet_link_file_name = datetime.now().strftime("%Y%m%d%H%M%S") \
        + '_magnet.txt'
    with open(result_name, 'w') as fd:
        for _s in result:
            fd.write(_s + '\n')

    with open(magnet_link_file_name, 'w') as fd:
        for _s in magnet_link_list:
            print(_s)
            fd.write(_s + '\n')

main_flow()




















