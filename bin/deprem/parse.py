#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import datetime
import time
import json


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
