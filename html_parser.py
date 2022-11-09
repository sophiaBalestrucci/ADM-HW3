import os 
import beautifulSoup4
import bs4
from pdb import set_trace
from datetime import datetime
import pandas  as pd 

class htmlParser():
    HTML_FILES = "datas/htmls/"

    def __init__(self) -> None:
        self.html_files = os.listdir(htmlParser.HTML_FILES)
        self.dataframe = pd.read_csv("datas/urls.csv")
        self.dataframe.NAME = self.dataframe.NAME.str.strip()
        self.process_pages()



    def read_file(self,file_name:str) -> bs4.BeautifulSoup:
        file_path = htmlParser.HTML_FILES + file_name

        with open(file_path,"r") as f:
            html = f.read()
        return bs4.BeautifulSoup(html,"html.parser")


    def extract_header_information(self,soup:bs4.BeautifulSoup):
        roi_header = soup.find_all("div", {"class": "DDPage__header-container grid-row"})[0]
        self.placeName = roi_header.find("h1", {"class":"DDPage__header-title"}).text.strip()

        location = roi_header.find("div", {"class":"DDPage__header-place-location"}).text.strip()

        counters = roi_header.find_all("div",{"class":"title-md item-action-count"})
        self.numPeopleVisited,self.numPeopleWant = int(counters[0].text.strip()),int(counters[1].text.strip())
        self.placeShortDesc = roi_header.find("h3", {"class":"DDPage__header-dek"}).text.strip()
        # set_trace(header="header infos")
    def extract_descriptions(self,soup:bs4.BeautifulSoup):

        ## Main Descriptions 
        placeDesc = soup.find_all("div", {"class": "DDP__body-copy"})[0]
        self.placeDesc = "".join([p.text.strip() for p in placeDesc.find_all("p")])
        # set_trace(header="descriptions")
    
    def extract_sidebar(self,soup:bs4.BeautifulSoup):
        sidebar = soup.find("div", {"class":"DDPageSiderail"})
        nearby_places = sidebar.find_all("div",{"class":"DDPageSiderailRecirc__item-title"})
        self.placeNearby = [place.text for place in nearby_places]
        self.placeAddress =  sidebar.find("address",{"class":"DDPageSiderail__address"}).find("div",recursive=False).get_text(" ").replace("\n","")

        positions =  sidebar.find("div",{"class":"DDPageSiderail__coordinates js-copy-coordinates"}).attrs["data-coordinates"].split(",")

        self.placeAlt, self.placeLong = float(positions[0].strip()), float(positions[1].strip())
        
    def extract_footer(self,soup:bs4.BeautifulSoup):
        footer = soup.find("div", {"id":"ugc-module"})
        Editors = footer.find_all("a",{"class":"DDPContributorsList__contributor"})

        self.placeEditors = [editors.find("span").text if editors.find("span") else editors.text for editors in Editors]
        placePubDate = footer.find("div",{"class":"DDPContributor__name"}).text
        self.placePubDate = datetime.strptime(placePubDate,"%B %d, %Y")
        self.placeTags = [item.get_text("").replace("\n","") for item in soup.find_all("a",{"class":"itemTags__link js-item-tags-link"})]

        # set_trace(header="sidebar")

    def extract_related_places(self,soup:bs4.BeautifulSoup):
        
        related_list = soup.find("div",{
            "class":"card-grid CardRecircSection__card-grid js-inject-gtm-data-in-child-links",
            "data-gtm-template":"DDP Footer Recirc Lists"
        })
        related_places = soup.find("div",{
            "class":"card-grid CardRecircSection__card-grid js-inject-gtm-data-in-child-links",
            "data-gtm-template":"DDP Footer Recirc Related"
        })
        self.placeRelatedLists = [data.find("span").text.strip() for data in related_list.find_all("h3")]
        self.placeRelatedPlaces = [data.find("span").text.strip() for  data in related_places.find_all("h3")]
        
    def process_pages(self):
        
        for idx,file_name in enumerate(self.html_files):
            try:
                soup = self.read_file(file_name=file_name)
                self.extract_header_information(soup=soup)
                self.extract_descriptions(soup=soup)
                self.extract_sidebar(soup=soup)
                self.extract_footer(soup=soup)
                self.extract_related_places(soup=soup)
                self.placeUrl = self.dataframe.loc[self.dataframe.NAME == self.placeName]["URL"]
                self.save_tsv_file(idx)
            except Exception as e : 
                print(e)
                set_trace()
    def save_tsv_file(self,idx:int):
        with open(f"datas/tsv_files/place_{idx}.tsv","w") as f:
            whole_data = [
                self.placeName,str(self.placeTags),str(self.numPeopleVisited),
                str(self.numPeopleWant),self.placeDesc,self.placeShortDesc,
                str(self.placeNearby),self.placeAddress,str(self.placeAlt),
                str(self.placeLong),str(self.placeEditors),self.placePubDate.strftime("%Y-%m-%d"),
                str(self.placeRelatedLists),
                str(self.placeRelatedPlaces),self.placeUrl.values[0]]
            

            tsv = "\t".join(whole_data)
            f.write(tsv)
            


            



if __name__ == "__main__":
    htmlParser()

