from bs4 import BeautifulSoup
import requests
import logging
from pprint import pprint
import pandas as pd

logging.basicConfig(
    filename='seo.log', 
    filemode='w', 
    format='%(asctime)s - %(message)s',level=logging.INFO
)

class Downloader:
    def __init__(self, url):
        self.url = url
        self.list_for_df = []

    def load(self):
        page = requests.get(self.url)
        # logging.info(f"Status : {page.status_code}")
        self.soup = BeautifulSoup(page.content, 'html.parser', from_encoding="utf-8")
        # print(self.soup)

    def find(self, *args): #! Not clean
        for tag in args:
            if tag == "description": # data is not a list so no loop or getText() needed
                text = self.soup.find('meta', attrs={'name' : tag})["content"] 
                text_len = len(text)
                # Add new list with seo data to self.list_for_df
                self.list_for_df.append([self.url, tag, text, text_len])
            else:
                _ = self.soup.find_all(tag)
                for html_tag in _:
                    text = html_tag.getText()
                    text_len = len(text) # character count
                    # Add new list with seo data to self.list_for_df
                    self.list_for_df.append([self.url, tag, text, text_len])


    def create_df(self):
        columns = ["url", "html-tag" , "text", "character count"]
        df = pd.DataFrame(self.list_for_df, columns=columns)
        return print(df)

        

        
    
        
if __name__ == "__main__":
    y = Downloader("https://kulturdata.de")
    y.load()
    y.find("title", "h1", "h2", "a", "description" )
    y.create_df()

    
    

