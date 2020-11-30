from bs4 import BeautifulSoup
import requests
import logging
from pprint import pprint
import pandas as pd
import sys
import networkx as nx
import matplotlib.pyplot as plt

logging.basicConfig(
    filename='seo.log', 
    filemode='w', 
    format='%(asctime)s - %(message)s',level=logging.INFO
)

def go(): # user interface for testing 
        go = input("Go on? y/n ")
        if go == "y":
            return True
        elif go == "n":
            return False
        else:
            go()     

class Downloader:
    def __init__(self):
        self.list_for_df = []
        self.link_list_set = set()
        self.scraped_list_set = set() # so I don't scrape urls twice 
        
        self.graph_links_with_text = []
    
    def load(self, url, domain):
        self.url = url
        self.domain = domain
        logging.info(f"URL : {self.url}")

        page = requests.get(self.url)
        logging.info(f"Status : {page.status_code}")
        self.soup = BeautifulSoup(page.content, 'html.parser', from_encoding="utf-8")
        self.scraped_list_set.add(self.url)

    def next_link(self):
        links_list_raw = self.soup.find_all("a")
        
        # check if link is internal, if so : add to set
        for link in links_list_raw:
            try:
                if (self.domain in link["href"]) and ("https" in link["href"]):
                    self.link_list_set.add(link["href"])

                    # Adding for Graph
                    self.graph_links_with_text.append([self.url, link["href"]])
                else:
                    pass
            except:
                pass
    
    def graph(self):
        df = pd.DataFrame(self.graph_links_with_text, columns=["from", "to"])
        G = nx.from_pandas_edgelist(df, source="from", target="to")
        nx.draw(G, with_labels=False)
        plt.show()

        



    def find(self, seo_tags):
        for tag in seo_tags:
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
    def recurs(self):
        print("Start")
        for link in self.link_list_set.copy():
            if str(link) in self.scraped_list_set.copy():
                pass
            else:
                self.load(link, domain)
                self.find(seo_tags)
                self.next_link()
        
        print(f"🗳 Anzahl an gecrawlten Links : {len(self.scraped_list_set)}")        
        if go():
            print("Here we go again")
            self.recurs()
        else:
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
    url = "https://www.kulturdata.de"
    domain = "kulturdata.de"
    seo_tags = ["title", "description"]
    y = Downloader()
    y.load(url, domain)
    y.find(seo_tags)
    y.next_link()

    y.recurs()
    y.graph() # not that intereseting at the moment 
    y.create_df()
    

    
    

