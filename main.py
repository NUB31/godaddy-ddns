import os
import time

import requests
import schedule

print("Starting ddns service")

domain = os.getenv('DOMAIN')
host = os.getenv('HOST')
APIKey = os.getenv('API_KEY')
APISecret = os.getenv('API_SECRET')


if (domain == None or host == None or APIKey == None or APISecret == None or domain == "" or host == "" or APIKey == "" or APISecret == ""):
    raise Exception(
        "Env variables not defined, reuqired variables are: DOMAIN, HOST, API_KEY and API_SECRET")

print("Service started successfully", flush=True)


def getWanIp():
    res = requests.get("https://api.ipify.org")
    print(f"fetching my ip, result: {res.text}", flush=True)
    return res.text


def getDnsIp():
    res = requests.get(f"https://api.godaddy.com/v1/domains/{domain}/records/A/{host}", headers={
                       "Authorization": f"sso-key {APIKey}:{APISecret}"})
    if res.json()[0]["data"]:
        ip = res.json()[0]["data"]
    else:
        raise Exception(
            f"No matching DNS records on domain: {domain} and host: {host}")

    print(f"fetching dns ip, result: {ip}", flush=True)
    return ip


def updateDnsIp(ip):
    url = f"https://api.godaddy.com/v1/domains/{domain}/records/A/{host}"
    headers = {"Authorization": f"sso-key {APIKey}:{APISecret}",
               "Content-Type": "application/json; charset=utf-8"}
    data = [{"data": ip}]

    res = requests.put(url, json=data, headers=headers)

    if res.ok:
        print(
            f"Successfully changed dns record, new dns record: {ip}", flush=True)


def job():
    wanIp = getWanIp()
    dnsIp = getDnsIp()

    if (wanIp != dnsIp) and (dnsIp != ""):
        print(
            "Found non-matching ips, attempting to change DNS record", flush=True)
        updateDnsIp(wanIp)
    else:
        print("Found matching ips, no changes necessary", flush=True)


schedule.every(10).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
