import requests
r = requests.get("https://stellic.floridapoly.edu/", 
 headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "cookie": "_shibsession_64656661756c7468747470733a2f2f666c6f72696461706f6c792e7374656c6c69632e636f6d2f73686962626f6c657468=_786d053a1ccad5e44330e8501c8647bd; csrftoken=o5auTWIKco8vlXGWM1TrVncCfREaxXViPjh3HTc0P3oyZWXsiwdHXvOBfMKsnOad; sessionid=hwtfag16ew649j6gn43igqzkifl1sd3w; _ga_6GN9LLBKF8=GS1.1.1734491402.1.0.1734491402.0.0.0; _ga=GA1.1.1881353146.1734491402; _ga_6VFQE788X7=GS1.1.1734491402.1.0.1734491402.0.0.0; _ga=GA1.3.1881353146.1734491402; _gid=GA1.3.1564221276.1734491402"
  },
)

print(r.text)