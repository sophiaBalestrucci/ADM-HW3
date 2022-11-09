#Importing needed libraries 
import pandas as pd 
from pdb import set_trace
import requests
import os 
import json
from typing import Dict
from time import sleep
import random

class htmlDownloader():
    def __init__(self,file_path:str="datas/urls.csv") -> None:
        self.urls = self._url_reader(file_path)

    def _url_reader(self,path:str,format_file="csv") -> pd.DataFrame :
        if format_file =="txt" :
            return pd.read_csv(path,sep=" ")
        return pd.read_csv(path)
        
    def download_htmls(self) -> None :
        config = self.last_download_control()
        roi_urls = self.urls.iloc[config["last_downloaded"]:]
        for idx,row in roi_urls.iterrows():
            try:
                print(f"Downloading {row.NAME}")
                sleep(random.randint(0,2))
                htmls = requests.get(row.URL).content
                saving_path = f"datas/htmls/{row.NAME}.html"
                with open(saving_path,"wb") as f:
                    f.write(htmls)
                config["last_downloaded"] += 1 

                if idx % 10 == 0 :
                    self.save_config_file(config)
            except Exception as e:
                print(f"ERROR {e}")
                self.save_config_file(config=config)
                    

    
    def last_download_control(self) -> Dict[str,int]:

        if os.path.isfile("config.json"):
            with open("config.json","rb") as f :
                config = json.load(f)
        else:
            config = {"last_downloaded":0}
            with open("config.json","w") as f:
                json.dump(config,f)
        return config

    def save_config_file(self,config:Dict[str,int]):
        with open("config.json","w") as f:
            json.dump(config,f)

    
if __name__ == "__main__":
    downloader = htmlDownloader()
    downloader.download_htmls()