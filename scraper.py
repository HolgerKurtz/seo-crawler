from bs4 import BeautifulSoup
import requests
import logging
from pprint import pprint

logging.basicConfig(
    filename='seo.log', 
    filemode='w', 
    format='%(asctime)s - %(message)s',level=logging.INFO
)

class Downloader:
    def __init__(self, url):
        self.url = url

    def load(self):
        page = requests.get(self.url)
        # logging.info(f"Status : {page.status_code}")
        self.soup = BeautifulSoup(page.content, 'html.parser', from_encoding="utf-8")
        # print(self.soup)

    def find(self, *args):
        _dict = {}
        for tag in args:
            text_list = []
            _ = self.soup.find_all(tag)
            
            for html_tag in _:
                text = html_tag.getText()
                # print(f"{tag} : {text}")
                text_list.append(text)
            _dict[tag] = text_list

        pprint(_dict)
