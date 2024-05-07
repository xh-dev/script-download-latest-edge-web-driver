import os

from bs4 import BeautifulSoup
from requests import Session
import re
import zipfile
from os import path
import shutil

edge_driver_name = "msedgedriver.exe"


def is_latest_version(version: str):
    if path.exists(".version"):
        v=""
        with open(".version", "r") as f:
            v = f.read()
        if v == version and path.exists(edge_driver_name):
            return True
        else:
            return False
    else:
        with open(".version", "w") as f:
            f.write(version)
        return False




if __name__ == '__main__':
    session = Session()
    resp=session.get("https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH#downloads")
    resp_text=resp.text
    soup = BeautifulSoup(resp_text,'html.parser')
    res = [ r for r in soup.select("div.block-web-driver__card") if r.select_one("h3").text == "Stable Channel"][0]
    text = res.select_one("div.block-web-driver__versions").text.replace("\r\n","\n").replace("\n"," ").replace(" +"," ")
    reg = re.compile("Version +([\\d+.]+) ")
    version = reg.match(text).group(1)
    print("latest version: ", version)

    if is_latest_version(version):
        print("Already latest version")
        exit(0)

    url_to_download=""
    for l in res.select("div.block-web-driver__version-links a"):
        if(l.text.strip() == "x64"):
            url_to_download=l.get("href").strip()

    resp = session.get(url_to_download)

    base_path="downloads"
    if not path.exists(base_path):
        os.mkdir(base_path)

    zip_name=f"{base_path}/msedgedriver.zip"

    if(resp.status_code == 200):
        with open(zip_name, "wb") as f:
            f.write(resp.content)
    else:
        print("fail download")

    with zipfile.ZipFile(zip_name, "r") as zip:
        zip.extractall(base_path)

    if path.exists(edge_driver_name):
        os.remove(edge_driver_name)
    os.rename(f"{base_path}/{edge_driver_name}",edge_driver_name)
    shutil.rmtree(base_path)







