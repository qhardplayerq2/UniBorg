import asyncio
import datetime
import json
import logging
import time
from datetime import datetime

import requests
from telethon import events

from bs4 import BeautifulSoup
# from bin.deprem.parse import (create_dict, get_content, get_html_line,
#                               get_json, get_timestamp, main, parse_html_line)
from uniborg.util import admin_cmd

# from bin.deprem.parse import *

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


URL="http://www.koeri.boun.edu.tr/scripts/lst0.asp"
def get_timestamp(zaman,saat):
    zaman=zaman.split(".")
    saat=saat.split(":")
    dt=datetime.datetime(int(zaman[0]),int(zaman[1]),int(zaman[2]),int(saat[0]),int(saat[1]),int(saat[2]))
    dt=time.mktime(dt.timetuple())
    return dt

def get_content():
    data=requests.get(URL)
    data=data.content
    return data

def get_html_line(data_html):
    parse=BeautifulSoup(data_html, 'html.parser')
    parsed=parse.find("pre")
    parsed=str(parsed)
    parsed=parsed.split("\n")
    parsed=parsed[7:507]
    return(parsed)

def parse_html_line(data_parsed):
    zaman=data_parsed[:10]
    saat=data_parsed[11:19]
    timestamp=get_timestamp(zaman,saat)
    enlem=float(data_parsed[21:28])
    boylam=float(data_parsed[31:38])
    derinlik=float(data_parsed[45:49])
    buyukluk = float(data_parsed[60:63])
    yer=data_parsed[71:121]

    data_parsed=[zaman,saat,enlem,boylam,buyukluk,derinlik,yer]
    quake_dict={"time":zaman+"/"+saat,"latitude":enlem,"longitude":boylam,"depth":derinlik,"magnitude":buyukluk,"location":yer,"timestamp":timestamp}
    return quake_dict

def create_dict(quake_list):
    dat_json=[]

    for i in quake_list:
        dat_json.append((parse_html_line(i)))
    return {"result":dat_json}

def get_json(dat_json):
    test=dat_json
    #f=open("quakes.html","w")
    #json.dump((dat_json),f)
    #f.close()
    return (json.dumps(test))

def main():
    parse_=get_html_line(get_content())
    dat_json=create_dict(parse_)
    final=get_json(dat_json)
    return final

if __name__ == '__main__':
    print(main())
    

else:
    pass
    # print("ok")



@borg.on(admin_cmd(pattern=("deprem ?(.*)")))
async def deprem_(event):
    if event.fwd_from:
        return
    ana_list=create_list(get_json(get_quakes()))
    sorted_list=sort_magnitude(ana_list)
    # print("Earthquakes with magnetude bigger than 3.5:")
    # mesaj = print_touser(sorted_list,"")
    await event.edit(print_touser(sorted_list,""))



liste_big=[]
def get_by_key_to_list(data,key):
    wanted_values=[]
    for i in data:
        wanted_values.append(i.get(key))
    return wanted_values


def sort_magnitude(data):
    sorted_list= sorted(data, key=lambda k: k['magnitude'])
    return sorted_list

def print_touser(data,setting):
    data.reverse()
    for i in data:
        if float(i.get("magnitude")) > 3.5 :
            print(i.get("magnitude"),i.get("location"),i.get("time"),sep="---")
            liste_big.append(i)
        elif setting=="all":
            print(i.get("magnitude"), i.get("location"), i.get("time"), sep="---")
        else:
            pass

def create_list(data_json):
    list_quakes=[]
    global gb_liste
    for i in range(0,len(data_json["result"])):
        list_quakes.append(data_json["result"][i])
    gb_liste=list_quakes
    return list_quakes

def get_json(data):
    dat_json=json.loads(data)
    return dat_json

def get_quakes():
    #URL="http://10.1.1.15/quake.html"
    #raw=requests.get(URL)
    #data=raw.content
   # return data
    res=parse.main()
    return res
