from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


def home(request):

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

    response = requests.get("https://visalist.io/emergency/coronavirus/india-country/maharashtra",headers=headers)

    content = response.content

    #BeautifulSoup Object Initialization
    soupobject = BeautifulSoup(content,"html.parser")

    cities = soupobject.find_all("div",attrs={"class": "v-list-item__content py-1"})
    
    citydata = []

    for city in range(len(cities)):

        citydict = {}

        try:
            citydict['cityname']=cities[city].find("div",attrs={"class":"layout"}).next_element.text.strip()
        except:
            citydict['cityname']=''

        try:
            citydict['newcases']=cities[city].find("span",attrs={"class":"v-list-item__action-text subtitle-1 bolder font-weight-bold pink--text text--accent-3"}).text.strip()
        except:
            citydict['newcases']=''

        try:
            citydict['activecases']=cities[city].find("span",attrs={"class":"pink--text text--accent-3"}).text
        except:
            citydict['activecases']=''

        try:
            citydict['recoveredcases']=cities[city].find("span",attrs={"class":"green--text text--accent-3"}).text.strip()
        except:
            citydict['recoveredcases']=''

        try:
            citydict['totaldeaths']=cities[city].find("span",attrs={"class":"grey--text"}).text.strip()
        except:
            citydict['totaldeaths']=''

        citydata.append(citydict)

        context = {"citydata": citydata}

    return render(request, 'index.html', context)
