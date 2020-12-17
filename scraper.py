from bs4 import BeautifulSoup
import requests
import logging
import pandas as pd
import sys
from random import randint
from time import sleep
from progress_bar import progress_bar # you need to pip install tqdm 

logging.basicConfig(
    filename='seo.log', 
    filemode='w', 
    format='%(asctime)s - %(message)s',level=logging.INFO
)

def go(): # user interface for testing 
        go = input("\n======> Go on? y/n ")
        if go == "y":
            return True
        elif go == "n":
            return False
        else:
            go()     

class Scraper:
    def __init__(self, domain):
        self.domain = domain
        self.list_for_df = []
        self.link_list_set = set()
        self.scraped_list_set = set() # so I don't scrape urls twice 
        self.graph_links_with_text = []
    
    def load(self, url):
        rand_sek = randint(0,2)
        sleep(rand_sek)
        self.url = url # dynamic for recursive calling with different urls 
        logging.info(f"URL : {self.url}")

        page = requests.get(self.url, verify=False)
        logging.info(f"Status : {page.status_code}")
        
        self.soup = BeautifulSoup(page.content, 'html.parser', from_encoding="utf-8")
        self.scraped_list_set.add(self.url)
        try:
            not_indexable = self.soup.find('meta', attrs={'name' : "robots"})["content"] # if indexable then == None
            if "noindex" in not_indexable:
                print(f"🤖 --> {not_indexable}")
                return True
            else:
                return False
        except:
            return False

    def next_link(self):
        links_list_raw = self.soup.find_all("a")
        # check if link is internal, if so : add to set
        for link in links_list_raw:
            try:
                if (self.domain in link["href"]) and ("https" in link["href"]):
                    self.link_list_set.add(link["href"])
                    self.graph_links_with_text.append([self.url, link["href"]]) # for graph()

                elif link["href"].startswith("/"): # relative paths like /impressum instead of www.domain.de/impressum
                    rel_path = "https://www." + self.domain + link["href"]
                    self.link_list_set.add(rel_path)
                    self.graph_links_with_text.append([self.url, rel_path])

                else:
                    pass
            except:
                pass
        logging.info(f"{len(links_list_raw)} Links found : \n{links_list_raw}")
    
    def graph(self):
        # Excel for Visualization with Gephi
        # See https://searchengineland.com/easy-visualizations-pagerank-page-groups-gephi-265716 
        df = pd.DataFrame(self.graph_links_with_text, columns=["Source", "Target"])
        self.create_csv(df, "seo-graph.csv")

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
    def progress_info(self):
        # Show the progress 
        self.amount = len(self.link_list_set)
        scraped = len(self.scraped_list_set)
        print(f"=====\nOverall Progress for {self.domain}")
        progress_bar(scraped, self.amount)
        old = 0

        for link in self.link_list_set:
            if str(link) in self.scraped_list_set:
                old +=1 
            else:
                pass
        diff = self.amount - old
        print("=====")
        print(f"{diff} new links found and ready for scraping")

        if go():
            print("Let's go!")
            pass
        else:
            y.graph() # not that intereseting at the moment 
            # y.create_df()
            sys.exit()

    def recurs(self):
        self.progress_info()
        count = 0
        for link in self.link_list_set.copy():
            print(f"Link : {link}")
            count +=1
            progress_bar(count, self.amount)
            try:
                if str(link) in self.scraped_list_set.copy():
                    pass
                elif self.load(link): # load(link) grabs robots to see if no-index in it if so, skip link
                    pass
                else:
                    self.load(link)
                    self.find(seo_tags)
                    
                    df = self.create_df()
                    self.create_csv(df, "seo.csv", "a", False)

                    self.next_link()
                    
            except:
                print(f"❌ Status Code für Link {link}")      
        
        # Starting again 
        self.recurs()

    def create_df(self):
        columns = ["url", "html-tag" , "text", "character count"]
        df = pd.DataFrame(self.list_for_df, columns=columns)
        return df
    
    def create_csv(self, df, filename, mode="w", header=True):
        df.to_csv(filename, mode=mode, header=header)
        print(f"Excel File created. Filename: {filename}")
    
        
if __name__ == "__main__":
    # Variables to choose
    url = "https://www.onelogic.de"
    domain = "onelogic.de"
    seo_tags = ["title", "description", "h1" , "h2", "h3"]

    # initial scrape
    y = Scraper(domain)
    y.load(url)
    y.find(seo_tags)
    df = y.create_df()
    y.create_csv(df, "seo.csv")
    y.next_link()

    # starting the Recursion to loop through internal links
    y.recurs()
    

    
    

