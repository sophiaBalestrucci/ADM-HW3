import requests
from pdb import set_trace
import bs4
import pandas as pd 
import random
from time import sleep
from typing import List

class urlDownloader():
    WEBSITE = "https://www.atlasobscura.com/places?page={}&sort=likes_count"

    def __init__(self,number_of_pages:int=400) -> None:
        self.number_of_pages = number_of_pages
    

    def _retriveTitle(self,soup_tags:bs4.element.Tag) -> str:
        title =soup_tags.find("h3").text
        if title is not None:
            return title
        return ""
    def _retrieveLink(self,soup_tags:bs4.element.Tag) -> str: 
        link = soup_tags.find("a").attrs["href"]
        if link is not None:
            return link
        return ""

    def saver_format(self,data:List[tuple],format:str=None):
        """_summary_

        Args:
            format (str, optional): _description_. Defaults to None.
        """
        data = pd.DataFrame(data,columns=["NAME","URL"])
        data["URL"] = "https://www.atlasobscura.com" + data.URL
        if format == "csv":
            data.to_csv("datas/urls.csv",index=False)
        if format == "txt":
            with open("datas/urls.txt","w") as f:
                for idx,row in data.iterrows():
                    f.write(" ".join(row.values)+"\n")

    def download_urls(self) -> pd.DataFrame:
        data_holder:List[tuple] = [] 
    
        for page_number in range(1,self.number_of_pages+1):
            sleep(random.randint(0,2))
            data = requests.get(urlDownloader.WEBSITE.format(page_number))
            soup = bs4.BeautifulSoup(data.content,features="lxml")
            roi_places = soup.find_all("div", {"class": "col-md-4 col-sm-6 col-xs-12"})#18
            for place in roi_places: 
                place_title = self._retriveTitle(place)
                place_link= self._retrieveLink(place)
                data_holder.append((place_title,place_link))
        self.saver_format(data=data_holder,format="csv")

            
if __name__ == "__main__":
    downloader = urlDownloader(number_of_pages=2)
    downloader.download_urls()
    
     