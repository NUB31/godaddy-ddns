import os
import time

import requests
import schedule
from dotenv import load_dotenv

load_dotenv()

domain = os.getenv('DOMAIN')
host = os.getenv('HOST')
APIKey = os.getenv('API_KEY')
APISecret = os.getenv('API_SECRET')

if (domain == None or host == None or APIKey == None or APISecret == None):
    raise Exception(
        "Env variables not defined, reuqired variables are: DOMAIN, HOST, API_KEY and API_SECRET")


def getWanIp():
    res = requests.get("https://api.ipify.org")
    print(f"fetching my ip, result: {res.text}")
    return res.text


def getDnsIp():
    res = requests.get(f"https://api.godaddy.com/v1/domains/{domain}/records/A/{host}", headers={
                       "Authorization": f"sso-key {APIKey}:{APISecret}"})
    ip = res.json()[0]["data"]
    print(f"fetching dns ip, result: {ip}")
    return ip


def updateDnsIp(ip):
    url = f"https://api.godaddy.com/v1/domains/{domain}/records/A/{host}"
    headers = {"Authorization": f"sso-key {APIKey}:{APISecret}",
               "Content-Type": "application/json; charset=utf-8"}
    data = [{"data": ip}]

    res = requests.put(url, json=data, headers=headers)

    if res.ok:
        print(f"Successfully changed dns record, new dns record: {ip}")


def job():
    wanIp = getWanIp()
    dnsIp = getDnsIp()

    if (wanIp != dnsIp) and (dnsIp != ""):
        print("Found non-matching ips, attempting to change DNS record")
        updateDnsIp(wanIp)
    else:
        print("Found matching ips, no changes necessary")


job()

schedule.every(10).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
