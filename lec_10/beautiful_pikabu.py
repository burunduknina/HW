import requests
from bs4 import BeautifulSoup
from collections import Counter


def pikabu_most_common_tags(cookies_value):
    pikabu_tags = Counter()
    cookies = {'pkbRem': cookies_value}
    with requests.Session() as s:
        for i in range(10):
            url = f'https://pikabu.ru/subs?page={i}'
            res = requests.get(url, headers=HEADERS, cookies=cookies)
            soup = BeautifulSoup(res.text, 'html.parser')
            all_tags = soup.find_all('a', {'class': 'tags__tag'})
            for n in all_tags:
                pikabu_tags[n.get_text()] += 1
    return pikabu_tags.most_common(10)


if __name__ == '__main__':
    HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                  "*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Cache-Control": 'no-cache',
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/'
                      '20100101 Firefox/71.0',
    }

    most_common_tags = pikabu_most_common_tags(input(
        'Please, enter cookies to connect: '))
    with open('pikabu_most_common_tags.txt', 'w', encoding='utf-8') as file:
        for tag in most_common_tags:
            file.write(f'{tag[0]}: {tag[1]}\n')
