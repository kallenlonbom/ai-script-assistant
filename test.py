
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def TestFunction(url):
    if not os.path.exists('output'):
        os.makedirs('output')

    to_visit = [url]
    visited = set()

    while to_visit:
        current_url = to_visit.pop(0)
        visited.add(current_url)

        response = requests.get(current_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        with open('output/' + current_url.replace('http://', '').replace('https://', '').replace('/', '_') + '.html', 'w', encoding='utf-8') as f_out:
            f_out.write(response.text)

        for link in soup.find_all('a'):
            absolute_link = urljoin(current_url, link.get('href'))
            if absolute_link.startswith(url) and absolute_link not in visited:
                to_visit.append(absolute_link)

TestFunction('http://example.com')
