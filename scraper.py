from bs4 import BeautifulSoup
import requests
import logging
from pprint import pprint
import pandas as pd
import sys

logging.basicConfig(
    filename='seo.log', 
    filemode='w', 
    format='%(asctime)s - %(message)s',level=logging.INFO
)

def go(): # user interface for testing 
        go = input("Go on? y/n ")
        if go == "y":
            pass
        elif go == "n":
            print("Done.")
            sys.exit()
        else:
            go()     

class Downloader:
    def __init__(self):
        self.list_for_df = []
        self.link_list_set = set()
        self.scraped_list_set = set() # so I don't scrape urls twice 
        

    def load(self, url):
        self.url = url
        logging.info(f"URL : {self.url}")

        page = requests.get(self.url)
        logging.info(f"Status : {page.status_code}")
        self.soup = BeautifulSoup(page.content, 'html.parser', from_encoding="utf-8")
        self.scraped_list_set.add(self.url)

    def next_link(self):
        print(f"🤖 next_link --> {self.url}")
        links_list_raw = self.soup.find_all("a")
        
        # check if link is internal, if so : add to set
        for link in links_list_raw:
            try:
                if self.url in link["href"]:
                    # print(link["href"])
                    self.link_list_set.add(link["href"])
            except:
                pass


    def find(self, *args): #! Not clean
        print(f"args/tags : {args} for {self.url}")
        for tag in args:
            try:
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
            except:
                pass


    def create_df(self):
        columns = ["url", "html-tag" , "text", "character count"]
        df = pd.DataFrame(self.list_for_df, columns=columns)
        logging.info(f"df.head() : \n{df.head()}")
        self.create_excel(df)
    
    def create_excel(self, df):
        filename = "seo.xlsx"
        df.to_excel(filename)
        print(f"Excel File created. Filename: {filename}")
    
        
if __name__ == "__main__":
    domain = "https://m.muenchenmusik.de"
    y = Downloader()
    y.load(domain)
    y.find("title", "description")
    y.next_link()
    y.create_df()
    

    
    

